#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <zlib.h>
#include <ctype.h>
#include <time.h>

// Calculate the Shannon entropy of a sequence
double shannon_entropy(char* sequence) {
    int counter[256] = {0};
    int len = strlen(sequence);
    for(int i = 0; i < len; i++) {
        counter[(int)sequence[i]]++;
    }
    double entropy = 0.0;
    for(int i = 0; i < 256; i++) {
        if(counter[i] > 0) {
            double p = (double)counter[i] / len;
            entropy -= p * log2(p);
        }
    }
    return entropy;
}

// Count the number of 'N' bases in the read
int count_n_bases(char* sequence) {
    int count = 0;
    int len = strlen(sequence);
    for(int i = 0; i < len; i++) {
        if(toupper(sequence[i]) == 'N') {
            count++;
        }
    }
    return count;
}

// Filters reads based on minimum sequence complexity and maximum number of 'N' bases allowed.
void filter_reads(const char* input_file, const char* output_file, double min_complexity, int max_n_bases, int truncate_end_bases) {
    gzFile fp = gzopen(input_file, "r");
    gzFile out_handle = gzopen(output_file, "w");
    if (fp == NULL || out_handle == NULL) {
        fprintf(stderr, "Failed to open file.\n");
        exit(EXIT_FAILURE);
    }

    char* line = NULL;
    size_t len = 0;
    ssize_t read;
    while ((read = gzgets(fp, line, sizeof(line))) != NULL) {
        // Allocate buffers dynamically based on the line length
        char* name = strdup(line);
        read = gzgets(fp, line, sizeof(line));
        char* seq = strdup(line);
        read = gzgets(fp, line, sizeof(line));
        char* plus = strdup(line);
        read = gzgets(fp, line, sizeof(line));
        char* qual = strdup(line);

        // Remove newlines from end of each line
        name[strcspn(name, "\n")] = 0;
        seq[strcspn(seq, "\n")] = 0;
        plus[strcspn(plus, "\n")] = 0;
        qual[strcspn(qual, "\n")] = 0;

        // Truncate the sequence
        int length = strlen(seq);
        if (length > truncate_end_bases) {
            seq[length - truncate_end_bases] = '\0';
            qual[length - truncate_end_bases] = '\0';
        }

        // Calculate entropy and count 'N' bases
        double entropy = shannon_entropy(seq);
        int n_bases = count_n_bases(seq);

        // Filter based on entropy and 'N' bases
        if (entropy >= min_complexity && n_bases <= max_n_bases) {
            gzprintf(out_handle, "%s\n%s\n%s\n%s\n", name, seq, plus, qual);
        }

        // Free the allocated buffers
        free(name);
        free(seq);
        free(plus);
        free(qual);
    }

    gzclose(fp);
    gzclose(out_handle);
}

int main(int argc, char *argv[]) {
    
    if(argc < 6) {
        printf("Usage: %s <input_file> <output_file> <min_complexity> <max_n_bases> <truncate_end_bases>\n", argv[0]);
        return 1;
    }

    char* input_file = argv[1];
    char* output_file = argv[2];
    double complexity = atof(argv[3]);
    int n_bases = atoi(argv[4]);
    int truncate_end_bases = atoi(argv[5]);
    clock_t start = clock();
    filter_reads(input_file, output_file, complexity, n_bases, truncate_end_bases);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken: %f seconds\n", time_taken);
    return 0;
}