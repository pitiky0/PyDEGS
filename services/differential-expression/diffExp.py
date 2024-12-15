import os
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import seaborn as sns
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import dendrogram, linkage
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from pydeseq2.default_inference import DefaultInference


# Set up and Configure logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
DIFF_EXPRESSION_EXCHANGE = os.getenv("DIFF_EXPRESSION_EXCHANGE", "diff_expression_exchange")
DIFF_EXPRESSION_QUEUE = os.getenv("DIFF_EXPRESSION_QUEUE", "diff_expression_queue")
FILES_MANAGEMENT_SERVICE = os.getenv("FILES_MANAGEMENT_SERVICE", "http://localhost:8003/files")

def get_file_path(file_name):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)
    return file_path

def download_file(type: str, file_name: str):
    if type == "couts":
        url = f"{FILES_MANAGEMENT_SERVICE}/quantification-files/download_file/?file_name={file_name}"
    else:
        url = f"{FILES_MANAGEMENT_SERVICE}/study-metadata-files/download_file/?file_name={file_name}"
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Ensure we notice bad responses

    file_path = get_file_path(file_name)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    logger.info(f"File downloaded to {file_path}")
    return file_path

def upload_file(file_path, user_id, folder_name):
    url = f"{FILES_MANAGEMENT_SERVICE}/def-expression-files/upload_file/?user_id={user_id}&folder_name={folder_name}"
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raise exception for non-200 status codes

    logger.info(f"File uploaded to {url}")
    return response.json()  # Assuming response is JSON

def add_tags_to_file(file_name, user_id):
    url = f"{FILES_MANAGEMENT_SERVICE}/quantification-files/add_tags/?file_name={file_name}"

    body = {'tags': {"analysed_by": f"{user_id}"}}

    response = requests.post(url, json=body)
    response.raise_for_status()  # Raise an error for bad status codes

    logger.info(f"Tags added to {file_name}")
    return response.json()

def get_file_tags(file_name):
    url = f"{FILES_MANAGEMENT_SERVICE}/def-expression-files/get_tags/?file_name={file_name}"

    response = requests.get(url)
    # response.raise_for_status()  # Raise an error for bad status codes

    if response.status_code == 404:
        return {}

    return response.json()

def add_analyse_tags(file_name, tags):

    url = f"{FILES_MANAGEMENT_SERVICE}/def-expression-files/add_tags/?file_name={file_name}"
    body = {'tags': tags}

    response = requests.post(url, json=body)
    response.raise_for_status()  # Raise an error for bad status codes

    logger.info(f"Filtering tags added to {file_name}")
    return response.json()

def diff_exp(filename: str, metadata: str, conditions, output_path: str = './output_files'):
    # Set up output directory
    os.makedirs(output_path, exist_ok=True)
    # Load counts data
    counts = pd.read_csv(filename, sep='\t', index_col=0)

    # Preprocess counts data
    counts.columns = counts.columns.str.replace(r'\.[sb]am$', '', regex=True)
    counts.columns = counts.columns.str.replace(r'^out_dir/', '', regex=True)
    counts = counts[counts.sum(axis=1) > 0]

    # Create metadata DataFrame from sample details
    metadata = pd.read_csv(metadata, sep='\t')
    metadata['SampleID'] = counts.columns
    metadata.set_index('SampleID', inplace=True)

    # conditions = metadata.columns.values.tolist()

    # Transpose the counts DataFrame to match the DESeq2 format
    counts = counts.T

    # Create DESeqDataSet object
    inference = DefaultInference(n_cpus=8)  # Adjust number of CPUs as needed
    dds = DeseqDataSet(counts=counts, metadata=metadata, design_factors=conditions, refit_cooks=True,
                       inference=inference)

    # Run DESeq2 analysis
    dds.deseq2()

    # --- QC Plots ---

    # Dispersion Plot
    dispersions = dds.varm['dispersions']
    plt.figure(figsize=(10, 10))
    plt.scatter(range(len(dispersions)), dispersions)
    plt.xlabel('Genes')
    plt.ylabel('Dispersion')
    plt.title('Dispersion plot')
    plt.savefig(os.path.join(output_path, 'qc-dispersions.png'))

    # Sample Distance Heatmap
    # (RLog transformation is not directly available in PyDESeq2; using a simple log transformation for demonstration)
    rlog_data = np.log2(counts + 1)

    # Calculate sample distances
    sample_dists = pdist(rlog_data, metric='euclidean')
    sample_dist_matrix = linkage(sample_dists, method='ward')

    # Create a larger figure for the heatmap
    plt.figure(figsize=(15, 10))  # Adjust figsize to make the plot larger

    # Plot the dendrogram
    dendrogram(sample_dist_matrix, labels=rlog_data.index)
    plt.title('Sample Distance Matrix')

    # Save the plot
    plt.savefig(os.path.join(output_path, 'qc-heatmap-samples.png'))

    # Show the plot
    plt.show()

    dds.layers['log1p'] = np.log1p(dds.layers['normed_counts'])

    grapher = pd.DataFrame(dds.layers['log1p'].T,
                           index=dds.var_names, columns=dds.obs_names)
    # Create the clustermap
    clustermap = sns.clustermap(grapher, z_score=0, cmap='RdYlBu_r')

    # Save the clustermap
    clustermap.savefig(os.path.join(output_path, 'qc-heatmap-samples.png'))

    # Principal Components Analysis
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(rlog_data)
    metadata['PCA1'] = pca_result[:, 0]
    metadata['PCA2'] = pca_result[:, 1]

    n_condition = len(conditions)

    # Create a figure with 3 subplots, one below the other
    fig, axes = plt.subplots(n_condition, 1, figsize=(10, 10 * n_condition))

    if n_condition == 1:
        axes = [axes]
    for i, condition in enumerate(conditions):
        sns.scatterplot(ax=axes[i], x='PCA1', y='PCA2', data=metadata, hue=condition, palette='Dark2', s=100)
        axes[i].set_title(f'PCA Biplot by {condition}')

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Save the combined figure
    plt.savefig(os.path.join(output_path, 'qc-pca.png'))

    # Show the plot
    plt.show()

    # --- Differential Expression Analysis ---

    # Perform statistical analysis with the DeseqStats class
    stat_res = DeseqStats(dds, inference=inference)
    stat_res.summary()

    # Get differential expression results
    res_df = stat_res.results_df
    res_df = res_df.sort_values('padj')
    res_df.to_csv(os.path.join(output_path, 'diffexpr-results.csv'), index=True)

    # --- Visualization of Results ---

    # Histogram of p-values
    plt.figure(figsize=(10, 6))
    plt.hist(res_df['pvalue'].dropna(), bins=50, color='grey')
    plt.xlabel('P-value')
    plt.ylabel('Frequency')
    plt.title('Histogram of p-values')
    plt.savefig(os.path.join(output_path, 'pvalue_hist.png'))

    # Extract baseMean and log2FoldChange
    baseMean = res_df['baseMean']
    log2FoldChange = res_df['log2FoldChange']
    padj = res_df['padj']

    # Create the MA plot
    plt.figure(figsize=(15, 10))
    plt.scatter(baseMean, log2FoldChange, c='grey', s=20, alpha=0.5, label='Not Significant')  # All genes in grey
    plt.scatter(baseMean[padj < 0.05], log2FoldChange[padj < 0.05], c='red', s=20, alpha=0.8,
                label='Significant')  # Significant genes in red

    # save significant gene symbols for MA plot
    with open(os.path.join(output_path, 'MA_plot_Significant_gene_symbols.txt'), 'w') as f:
        for i, row in res_df.iterrows():
            if row['padj'] < 0.05:
                f.write(i + '\n')
        f.close()

    plt.xscale('log')  # Log scale for the x-axis (baseMean)
    plt.xlabel('Base Mean')
    plt.ylabel('Log2 Fold Change')
    plt.title('MA Plot')
    plt.legend()
    plt.savefig(os.path.join(output_path, 'diffexpr-maplot.png'))
    plt.show()

    # Define thresholds
    lfcthresh = 1
    sigthresh = 0.05

    # Create the volcano plot
    plt.figure(figsize=(12, 10))
    plt.scatter(res_df['log2FoldChange'], -np.log10(res_df['pvalue']), c='grey', s=20, alpha=0.5,
                label='Not Significant')  # All genes in grey
    plt.scatter(res_df['log2FoldChange'][res_df['padj'] < sigthresh],
                -np.log10(res_df['pvalue'][res_df['padj'] < sigthresh]), c='red', s=20, alpha=0.8,
                label='FDR < 0.05')  # Significant genes in red
    plt.scatter(res_df['log2FoldChange'][np.abs(res_df['log2FoldChange']) > lfcthresh],
                -np.log10(res_df['pvalue'][np.abs(res_df['log2FoldChange']) > lfcthresh]), c='orange', s=20, alpha=0.8,
                label='|LogFC| > 1')  # Genes with |LogFC| > 1 in orange
    plt.scatter(res_df['log2FoldChange'][(res_df['padj'] < sigthresh) & (np.abs(res_df['log2FoldChange']) > lfcthresh)],
                -np.log10(
                    res_df['pvalue'][(res_df['padj'] < sigthresh) & (np.abs(res_df['log2FoldChange']) > lfcthresh)]),
                c='green', s=20, alpha=0.8, label='Both')  # Genes meeting both criteria in green

    # save significant gene symbols for volcano plot
    with open(os.path.join(output_path, 'Volcano_plot_Significant_gene_symbols.txt'), 'w') as f:
        for i, row in res_df.iterrows():
            if (row['padj'] < sigthresh) and (np.abs(row['log2FoldChange']) > lfcthresh):
                f.write(i + '\n')
        f.close()

    plt.xlabel('Log2 Fold Change')
    plt.ylabel('-Log10 P-value')
    plt.title('Volcano Plot')
    plt.legend()
    plt.xlim([-2.3, 2.3])
    plt.savefig(os.path.join(output_path, 'diffexpr-volcanoplot.png'))
    plt.show()

def perform_diff_expression(file_name, user_id, metadata, conditions):
    # check if the file is already controled or not
    folder = file_name.replace("_counts.txt", "")

    analysed_file_name = f"{folder}/diffexpr-results.csv"
    body = get_file_tags(analysed_file_name)
    if "tags" in body.keys():
        if body['tags']['origin_file'] == file_name:
            logger.info(f"File {file_name} already analysed")
            return

    file_path = download_file("couts", file_name)
    metadata = download_file("metadata", metadata)

    diff_exp(file_name, metadata, conditions)

    # Loop through all files in the output_dir
    for file in os.listdir('./output_files'):
        output_file_path = os.path.join('./output_files', file)
        try:
            upload_response = upload_file(output_file_path, user_id, folder)
            add_analyse_tags(f"{folder}/{file}", {'origin_file':file_name})
            logger.info(f"Upload successful. Response: {upload_response}")
        except requests.exceptions.RequestException as e:
            logger.info(f"Upload failed: {e}")

    add_tags_to_file(file_name, user_id)

    # Remove the downloaded file
    os.remove(file_name)

    # Remove the output directory and all its contents
    os.system("rm -r ./output_files")
