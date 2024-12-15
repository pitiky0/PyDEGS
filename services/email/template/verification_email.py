def get_formated_text(app_name, email, token, auth_service):
    body_text = f"""
    Please verify your email 😀
    
    To use {app_name}, click the verification button. This helps keep your account secure.
    
    Verify my account ( {auth_service}/profile/verify-email?email={email}&token={token} )
    
    You're receiving this email because you have an account in {app_name}. If you are not sure why you're receiving this, please contact us by replying to this email.
    
    {app_name} is a user-friendly platform designed to simplify the analysis of RNA sequencing data, enabling researchers to easily identify genes that are differentially expressed between different biological conditions.
    
    """
    return body_text

def get_formated_html(app_name, email, token, auth_service):

    body_html = f"""
    <!--
    * This email was built using Tabular.
    * For more information, visit https://tabular.email
    -->
    <!DOCTYPE html
        PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml"
        xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">

    <head>
        <title></title>
        <meta charset="UTF-8" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <!--[if !mso]>-->
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <!--<![endif]-->
        <meta name="x-apple-disable-message-reformatting" content="" />
        <meta content="target-densitydpi=device-dpi" name="viewport" />
        <meta content="true" name="HandheldFriendly" />
        <meta content="width=device-width" name="viewport" />
        <meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no" />
        <style type="text/css">
            table {{
                border-collapse: separate;
                table-layout: fixed;
                mso-table-lspace: 0;
                mso-table-rspace: 0;
            }}

            table td {{
                /*add same lines */
                border-collapse: collapse;
                mso-table-lspace: 0;
                mso-table-rspace: 0;
            }}

            .ExternalClass {{
                width: 100%
            }}

            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {{
                line-height: 100%
            }}

            body,
            a,
            li,
            p,
            h1,
            h2,
            h3 {{
                -ms-text-size-adjust: 100%;
                -webkit-text-size-adjust: 100%;
            }}

            html {{
                -webkit-text-size-adjust: none !important
            }}

            body,
            #innerTable {{
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale
            }}

            #innerTable img+div {{
                display: none;
                display: none !important
            }}

            img {{
                Margin: 0;
                padding: 0;
                -ms-interpolation-mode: bicubic
            }}

            h1,
            h2,
            h3,
            p,
            a {{
                line-height: inherit;
                overflow-wrap: normal;
                white-space: normal;
                word-break: break-word
            }}

            a {{
                text-decoration: none
            }}

            h1,
            h2,
            h3,
            p {{
                min-width: 100% !important;
                width: 100% !important;
                max-width: 100% !important;
                display: inline-block !important;
                border: 0;
                padding: 0;
                margin: 0
            }}

            a[x-apple-data-detectors] {{
                color: inherit !important;
                text-decoration: none !important;
                font-size: inherit !important;
                font-family: inherit !important;
                font-weight: inherit !important;
                line-height: inherit !important
            }}

            u+#body a {{
                color: inherit;
                text-decoration: none;
                font-size: inherit;
                font-family: inherit;
                font-weight: inherit;
                line-height: inherit;
            }}

            a[href^="mailto"],
            a[href^="tel"],
            a[href^="sms"] {{
                color: inherit;
                text-decoration: none
            }}

            img,
            p {{
                margin: 0;
                Margin: 0;
                font-family: Lato, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 22px;
                font-weight: 400;
                font-style: normal;
                font-size: 16px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: left;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}

            h1 {{
                margin: 0;
                Margin: 0;
                font-family: Inter Tight, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 34px;
                font-weight: 700;
                font-style: normal;
                font-size: 28px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: center;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}

            h2 {{
                margin: 0;
                Margin: 0;
                font-family: Lato, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 30px;
                font-weight: 400;
                font-style: normal;
                font-size: 24px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: left;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}

            h3 {{
                margin: 0;
                Margin: 0;
                font-family: Lato, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 26px;
                font-weight: 400;
                font-style: normal;
                font-size: 20px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: left;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}
        </style>
        <style type="text/css">
            @media (min-width: 481px) {{
                .hd {{
                    display: none !important
                }}
            }}
        </style>
        <style type="text/css">
            @media (max-width: 480px) {{
                .hm {{
                    display: none !important
                }}
            }}
        </style>
        <style type="text/css">
            @media (min-width: 481px) {{

                h1,
                img,
                p {{
                    margin: 0;
                    Margin: 0
                }}

                .t24,
                .t5 {{
                    width: 318px !important
                }}

                img,
                p {{
                    font-family: Lato, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                    line-height: 22px;
                    font-weight: 400;
                    font-style: normal;
                    font-size: 16px;
                    text-decoration: none;
                    text-transform: none;
                    letter-spacing: 0;
                    direction: ltr;
                    color: #333;
                    text-align: left;
                    mso-line-height-rule: exactly;
                    mso-text-raise: 2px
                }}

                h1 {{
                    font-family: Inter Tight, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                    line-height: 34px;
                    font-weight: 700;
                    font-style: normal;
                    font-size: 28px;
                    text-decoration: none;
                    text-transform: none;
                    letter-spacing: 0;
                    direction: ltr;
                    color: #333;
                    text-align: center;
                    mso-line-height-rule: exactly;
                    mso-text-raise: 2px
                }}

                h2,
                h3 {{
                    margin: 0;
                    Margin: 0;
                    font-family: Lato, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                    font-weight: 400;
                    font-style: normal;
                    text-decoration: none;
                    text-transform: none;
                    letter-spacing: 0;
                    direction: ltr;
                    color: #333;
                    text-align: left;
                    mso-line-height-rule: exactly;
                    mso-text-raise: 2px
                }}

                h2 {{
                    line-height: 30px;
                    font-size: 24px
                }}

                h3 {{
                    line-height: 26px;
                    font-size: 20px
                }}

                .t23,
                .t26 {{
                    mso-line-height-alt: 70px !important;
                    line-height: 70px !important;
                    display: block !important
                }}

                .t24 {{
                    padding-top: 50px !important;
                    border: 1px solid #cecece !important;
                    border-radius: 20px !important;
                    overflow: hidden !important
                }}

                .t20 {{
                    mso-line-height-alt: 30px !important;
                    line-height: 30px !important
                }}

                .t21 {{
                    width: 258px !important
                }}
            }}
        </style>
        <style type="text/css" media="screen and (min-width:481px)">
            .moz-text-html img,
            .moz-text-html p {{
                margin: 0;
                Margin: 0;
                font-family: Lato, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 22px;
                font-weight: 400;
                font-style: normal;
                font-size: 16px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: left;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}

            .moz-text-html h1 {{
                margin: 0;
                Margin: 0;
                font-family: Inter Tight, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 34px;
                font-weight: 700;
                font-style: normal;
                font-size: 28px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: center;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}

            .moz-text-html h2 {{
                margin: 0;
                Margin: 0;
                font-family: Lato, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 30px;
                font-weight: 400;
                font-style: normal;
                font-size: 24px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: left;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}

            .moz-text-html h3 {{
                margin: 0;
                Margin: 0;
                font-family: Lato, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 26px;
                font-weight: 400;
                font-style: normal;
                font-size: 20px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: left;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}

            .moz-text-html .t23,
            .moz-text-html .t26 {{
                mso-line-height-alt: 70px !important;
                line-height: 70px !important;
                display: block !important
            }}

            .moz-text-html .t24 {{
                padding-top: 50px !important;
                border: 1px solid #cecece !important;
                border-radius: 20px !important;
                overflow: hidden !important;
                width: 318px !important
            }}

            .moz-text-html .t5 {{
                width: 318px !important
            }}

            .moz-text-html .t20 {{
                mso-line-height-alt: 30px !important;
                line-height: 30px !important
            }}

            .moz-text-html .t21 {{
                width: 258px !important
            }}
        </style>
        <!--[if !mso]>-->
        <link
            href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&amp;family=Albert+Sans:wght@500&amp;display=swap"
            rel="stylesheet" type="text/css" />
        <!--<![endif]-->
        <!--[if mso]>
    <style type="text/css">
    img,p{{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:22px;font-weight:400;font-style:normal;font-size:16px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}h1{{margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:34px;font-weight:700;font-style:normal;font-size:28px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px}}h2{{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:30px;font-weight:400;font-style:normal;font-size:24px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}h3{{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:26px;font-weight:400;font-style:normal;font-size:20px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}div.t23,div.t26{{mso-line-height-alt:70px !important;line-height:70px !important;display:block !important}}td.t24{{padding-top:50px !important;border:1px solid #cecece !important;border-radius:20px !important;overflow:hidden !important}}div.t20{{mso-line-height-alt:30px !important;line-height:30px !important}}
    </style>
    <![endif]-->
        <!--[if mso]>
    <xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG/>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->
    </head>

    <body id="body" class="t29" style="min-width:100%;Margin:0px;padding:0px;background-color:#F9F9F9;">
        <div class="t28" style="background-color:#F9F9F9;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" align="center">
                <tr>
                    <td class="t27" style="font-size:0;line-height:0;mso-line-height-rule:exactly;background-color:#F9F9F9;"
                        valign="top" align="center">
                        <!--[if mso]>
    <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false">
    <v:fill color="#F9F9F9"/>
    </v:background>
    <![endif]-->
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" align="center"
                            id="innerTable">
                            <tr>
                                <td>
                                    <div class="t23" style="mso-line-height-rule:exactly;font-size:1px;display:none;">&nbsp;
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <!--[if !mso]>-->
                                    <table class="t25" role="presentation" cellpadding="0" cellspacing="0"
                                        style="Margin-left:auto;Margin-right:auto;">
                                        <!--<![endif]-->
                                        <!--[if mso]><table class="t25" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                        <tr>
                                            <!--[if !mso]>-->
                                            <td class="t24"
                                                style="background-color:#FFFFFF;width:320px;padding:43px 40px 40px 40px;">
                                                <!--<![endif]-->
                                                <!--[if mso]><td class="t24" style="background-color:#FFFFFF;width:400;padding:43px 40px 40px 40px;"><![endif]-->
                                                <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                                                    <tr>
                                                        <td>
                                                            <!--[if !mso]>-->
                                                            <table class="t2" role="presentation" cellpadding="0"
                                                                cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                                <!--<![endif]-->
                                                                <!--[if mso]><table class="t2" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                <tr>
                                                                    <!--[if !mso]>-->
                                                                    <td class="t1" style="width:60px;">
                                                                        <!--<![endif]-->
                                                                        <!--[if mso]><td class="t1" style="width:60;"><![endif]-->
                                                                        <a href="#" style="font-size:0px;"
                                                                            target="_blank"><img class="t0"
                                                                                style="display:block;border:0;height:auto;width:100%;Margin:0;max-width:100%;"
                                                                                width="60" height="60" alt=""
                                                                                src="https://6bc8d8a7-2411-4ec7-87eb-c1fd8615d533.b-cdn.net/e/9cb21986-5dcd-4ffa-8b86-afacbd68f834/db949bb7-445d-4aa1-8394-dd6f8d32ca9d.png" /></a>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <div class="t3"
                                                                style="mso-line-height-rule:exactly;mso-line-height-alt:40px;line-height:40px;font-size:1px;display:block;">
                                                                &nbsp;</div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <!--[if !mso]>-->
                                                            <table class="t6" role="presentation" cellpadding="0"
                                                                cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                                <!--<![endif]-->
                                                                <!--[if mso]><table class="t6" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                <tr>
                                                                    <!--[if !mso]>-->
                                                                    <td class="t5" style="width:320px;">
                                                                        <!--<![endif]-->
                                                                        <!--[if mso]><td class="t5" style="width:318;"><![endif]-->
                                                                        <h1 class="t4"
                                                                            style="margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:28px;font-weight:600;font-style:normal;font-size:24px;text-decoration:none;text-transform:none;letter-spacing:-1.2px;direction:ltr;color:#111111;text-align:center;mso-line-height-rule:exactly;mso-text-raise:1px;">
                                                                            Please verify your email 😀</h1>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <div class="t8"
                                                                style="mso-line-height-rule:exactly;mso-line-height-alt:17px;line-height:17px;font-size:1px;display:block;">
                                                                &nbsp;</div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <!--[if !mso]>-->
                                                            <table class="t10" role="presentation" cellpadding="0"
                                                                cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                                <!--<![endif]-->
                                                                <!--[if mso]><table class="t10" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                <tr>
                                                                    <!--[if !mso]>-->
                                                                    <td class="t9" style="width:308px;">
                                                                        <!--<![endif]-->
                                                                        <!--[if mso]><td class="t9" style="width:308;"><![endif]-->
                                                                        <p class="t7"
                                                                            style="margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:22px;font-weight:500;font-style:normal;font-size:15px;text-decoration:none;text-transform:none;letter-spacing:-0.6px;direction:ltr;color:#424040;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px;">
                                                                            To use {app_name}, click the verification button. This
                                                                            helps keep your account secure.</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <div class="t12"
                                                                style="mso-line-height-rule:exactly;mso-line-height-alt:40px;line-height:40px;font-size:1px;display:block;">
                                                                &nbsp;</div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <!--[if !mso]>-->
                                                            <table class="t14" role="presentation" cellpadding="0"
                                                                cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                                <!--<![endif]-->
                                                                <!--[if mso]><table class="t14" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                <tr>
                                                                    <!--[if !mso]>-->
                                                                    <td class="t13"
                                                                        style="background-color:#0057FF;overflow:hidden;width:141px;text-align:center;line-height:32px;mso-line-height-rule:exactly;mso-text-raise:5px;border-radius:8px 8px 8px 8px;">
                                                                        <!--<![endif]-->
                                                                        <!--[if mso]><td class="t13" style="background-color:#0057FF;overflow:hidden;width:141;text-align:center;line-height:32px;mso-line-height-rule:exactly;mso-text-raise:5px;border-radius:8px 8px 8px 8px;"><![endif]-->
                                                                        <a class="t11" href="{auth_service}/profile/verify-email?token={token}&email={email}"
                                                                            style="display:block;margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:32px;font-weight:700;font-style:normal;font-size:14px;text-decoration:none;letter-spacing:-0.5px;direction:ltr;color:#FFFFFF;text-align:center;mso-line-height-rule:exactly;mso-text-raise:5px;"
                                                                            target="_blank">Verify my account</a>
                                                                    </td>

                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <div class="t16"
                                                                style="mso-line-height-rule:exactly;mso-line-height-alt:40px;line-height:40px;font-size:1px;display:block;">
                                                                &nbsp;</div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <!--[if !mso]>-->
                                                            <table class="t18" role="presentation" cellpadding="0"
                                                                cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                                <!--<![endif]-->
                                                                <!--[if mso]><table class="t18" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                <tr>
                                                                    <!--[if !mso]>-->
                                                                    <td class="t17" style="width:318px;">
                                                                        <!--<![endif]-->
                                                                        <!--[if mso]><td class="t17" style="width:318;"><![endif]-->
                                                                        <p class="t15"
                                                                            style="margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:22px;font-weight:500;font-style:normal;font-size:14px;text-decoration:none;text-transform:none;letter-spacing:-0.6px;direction:ltr;color:#424040;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px;">
                                                                            You&#39;re receiving this email because you have
                                                                            an account in {app_name}. If you are not sure why
                                                                            you&#39;re receiving this, please contact us by
                                                                            replying to this email.</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <div class="t20"
                                                                style="mso-line-height-rule:exactly;mso-line-height-alt:26px;line-height:26px;font-size:1px;display:block;">
                                                                &nbsp;</div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <!--[if !mso]>-->
                                                            <table class="t22" role="presentation" cellpadding="0"
                                                                cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                                <!--<![endif]-->
                                                                <!--[if mso]><table class="t22" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                <tr>
                                                                    <!--[if !mso]>-->
                                                                    <td class="t21"
                                                                        style="background-color:#F2EFF3;overflow:hidden;width:260px;padding:20px 30px 20px 30px;border-radius:8px 8px 8px 8px;">
                                                                        <!--<![endif]-->
                                                                        <!--[if mso]><td class="t21" style="background-color:#F2EFF3;overflow:hidden;width:318;padding:20px 30px 20px 30px;border-radius:8px 8px 8px 8px;"><![endif]-->
                                                                        <p class="t19"
                                                                            style="margin:0;Margin:0;font-family:Albert Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:18px;font-weight:500;font-style:normal;font-size:12px;text-decoration:none;text-transform:none;direction:ltr;color:#84828E;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px;">
                                                                            <strong>{app_name}</strong> is a user-friendly platform
                                                                            designed to simplify the analysis of RNA sequencing data,
                                                                            enabling researchers to easily identify genes that are
                                                                            differentially expressed between different biological conditions.</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class="t26" style="mso-line-height-rule:exactly;font-size:1px;display:none;">&nbsp;
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </div>
    </body>

    </html>

    """
    return body_html
