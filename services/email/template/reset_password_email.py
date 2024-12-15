
def get_html_body(app_name, auth_service, token, email):
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
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt
        }}

        table td {{
            border-collapse: collapse
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
            font-family: Inter Tight, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
            line-height: 21px;
            font-weight: 500;
            font-style: normal;
            font-size: 16px;
            text-decoration: none;
            text-transform: none;
            letter-spacing: 0;
            direction: ltr;
            color: #19227d;
            text-align: center;
            mso-line-height-rule: exactly;
            mso-text-raise: 2px
        }}

        h1 {{
            margin: 0;
            Margin: 0;
            font-family: Roboto, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
            line-height: 34px;
            font-weight: 400;
            font-style: normal;
            font-size: 28px;
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

            img,
            p {{
                font-family: Inter Tight, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 21px;
                font-weight: 500;
                font-style: normal;
                font-size: 16px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #19227d;
                text-align: center;
                mso-line-height-rule: exactly;
                mso-text-raise: 2px
            }}

            h1 {{
                font-family: Roboto, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
                line-height: 34px;
                font-weight: 400;
                font-style: normal;
                font-size: 28px;
                text-decoration: none;
                text-transform: none;
                letter-spacing: 0;
                direction: ltr;
                color: #333;
                text-align: left;
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

            .t7 {{
                line-height: 41px !important;
                font-size: 35px !important
            }}
        }}
    </style>
    <style type="text/css" media="screen and (min-width:481px)">
        .moz-text-html img,
        .moz-text-html p {{
            margin: 0;
            Margin: 0;
            font-family: Inter Tight, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
            line-height: 21px;
            font-weight: 500;
            font-style: normal;
            font-size: 16px;
            text-decoration: none;
            text-transform: none;
            letter-spacing: 0;
            direction: ltr;
            color: #19227d;
            text-align: center;
            mso-line-height-rule: exactly;
            mso-text-raise: 2px
        }}

        .moz-text-html h1 {{
            margin: 0;
            Margin: 0;
            font-family: Roboto, BlinkMacSystemFont, Segoe UI, Helvetica Neue, Arial, sans-serif;
            line-height: 34px;
            font-weight: 400;
            font-style: normal;
            font-size: 28px;
            text-decoration: none;
            text-transform: none;
            letter-spacing: 0;
            direction: ltr;
            color: #333;
            text-align: left;
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

        .moz-text-html .t7 {{
            line-height: 41px !important;
            font-size: 35px !important
        }}
    </style>
    <!--[if !mso]>-->
    <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;900&amp;display=swap"
        rel="stylesheet" type="text/css" />
    <!--<![endif]-->
    <!--[if mso]>
<style type="text/css">
img,p{{margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:21px;font-weight:500;font-style:normal;font-size:16px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#19227d;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px}}h1{{margin:0;Margin:0;font-family:Roboto,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:34px;font-weight:400;font-style:normal;font-size:28px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}h2{{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:30px;font-weight:400;font-style:normal;font-size:24px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}h3{{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:26px;font-weight:400;font-style:normal;font-size:20px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}h1.t7{{line-height:41px !important;font-size:35px !important}}
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

<body id="body" class="t35" style="min-width:100%;Margin:0px;padding:0px;background-color:#292929;">
    <div class="t34" style="background-color:#292929;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" align="center">
            <tr>
                <td class="t33" style="font-size:0;line-height:0;mso-line-height-rule:exactly;background-color:#292929;"
                    valign="top" align="center">
                    <!--[if mso]>
<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false">
<v:fill color="#292929"/>
</v:background>
<![endif]-->
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" align="center"
                        id="innerTable">
                        <tr>
                            <td>
                                <div class="t29"
                                    style="mso-line-height-rule:exactly;mso-line-height-alt:60px;line-height:60px;font-size:1px;display:block;">
                                    &nbsp;</div>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <!--[if !mso]>-->
                                <table class="t31" role="presentation" cellpadding="0" cellspacing="0"
                                    style="Margin-left:auto;Margin-right:auto;">
                                    <!--<![endif]-->
                                    <!--[if mso]><table class="t31" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                    <tr>
                                        <!--[if !mso]>-->
                                        <td class="t30" style="width:400px;padding:0 20px 0 20px;">
                                            <!--<![endif]-->
                                            <!--[if mso]><td class="t30" style="width:440;padding:0 20px 0 20px;"><![endif]-->
                                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td>
                                                        <!--[if !mso]>-->
                                                        <table class="t6" role="presentation" cellpadding="0"
                                                            cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                            <!--<![endif]-->
                                                            <!--[if mso]><table class="t6" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                            <tr>
                                                                <!--[if !mso]>-->
                                                                <td class="t5"
                                                                    style="background-color:#CDD6B0;overflow:hidden;width:350px;padding:26px 25px 26px 25px;border-radius:14px 14px 0 0;">
                                                                    <!--<![endif]-->
                                                                    <!--[if mso]><td class="t5" style="background-color:#CDD6B0;overflow:hidden;width:400;padding:26px 25px 26px 25px;border-radius:14px 14px 0 0;"><![endif]-->
                                                                    <div class="t4"
                                                                        style="display:inline-table;width:100%;text-align:center;vertical-align:top;">
                                                                        <!--[if mso]>
<table role="presentation" cellpadding="0" cellspacing="0" align="center" valign="top" width="55"><tr><td width="55" valign="top"><![endif]-->
                                                                        <div class="t3"
                                                                            style="display:inline-table;text-align:initial;vertical-align:inherit;width:15.71429%;max-width:55px;">
                                                                            <table role="presentation" width="100%"
                                                                                cellpadding="0" cellspacing="0"
                                                                                class="t2">
                                                                                <tr>
                                                                                    <td class="t1">
                                                                                        <div style="font-size:0px;"><img
                                                                                                class="t0"
                                                                                                style="display:block;border:0;height:auto;width:100%;Margin:0;max-width:100%;"
                                                                                                width="55"
                                                                                                height="36.4375" alt=""
                                                                                                src="https://6bc8d8a7-2411-4ec7-87eb-c1fd8615d533.b-cdn.net/e/9cb21986-5dcd-4ffa-8b86-afacbd68f834/c2909bb6-42d0-4e9a-a701-cd67e1f6cea5.png" />
                                                                                        </div>
                                                                                    </td>
                                                                                </tr>
                                                                            </table>
                                                                        </div>
                                                                        <!--[if mso]>
</td>
</tr></table>
<![endif]-->
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <!--[if !mso]>-->
                                                        <table class="t24" role="presentation" cellpadding="0"
                                                            cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                            <!--<![endif]-->
                                                            <!--[if mso]><table class="t24" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                            <tr>
                                                                <!--[if !mso]>-->
                                                                <td class="t23"
                                                                    style="background-color:#FFFFFF;overflow:hidden;width:320px;padding:40px 40px 40px 40px;border-radius:0 0 14px 14px;">
                                                                    <!--<![endif]-->
                                                                    <!--[if mso]><td class="t23" style="background-color:#FFFFFF;overflow:hidden;width:400;padding:40px 40px 40px 40px;border-radius:0 0 14px 14px;"><![endif]-->
                                                                    <table role="presentation" width="100%"
                                                                        cellpadding="0" cellspacing="0">
                                                                        <tr>
                                                                            <td>
                                                                                <!--[if !mso]>-->
                                                                                <table class="t9" role="presentation"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="Margin-left:auto;Margin-right:auto;">
                                                                                    <!--<![endif]-->
                                                                                    <!--[if mso]><table class="t9" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                                    <tr>
                                                                                        <!--[if !mso]>-->
                                                                                        <td class="t8"
                                                                                            style="width:320px;">
                                                                                            <!--<![endif]-->
                                                                                            <!--[if mso]><td class="t8" style="width:320;"><![endif]-->
                                                                                            <h1 class="t7"
                                                                                                style="margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:35px;font-weight:900;font-style:normal;font-size:30px;text-decoration:none;text-transform:none;direction:ltr;color:#121212;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px;">
                                                                                                Forgot your password?
                                                                                            </h1>
                                                                                        </td>
                                                                                    </tr>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td>
                                                                                <div class="t11"
                                                                                    style="mso-line-height-rule:exactly;mso-line-height-alt:20px;line-height:20px;font-size:1px;display:block;">
                                                                                    &nbsp;</div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td>
                                                                                <!--[if !mso]>-->
                                                                                <table class="t13" role="presentation"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="Margin-left:auto;Margin-right:auto;">
                                                                                    <!--<![endif]-->
                                                                                    <!--[if mso]><table class="t13" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                                    <tr>
                                                                                        <!--[if !mso]>-->
                                                                                        <td class="t12"
                                                                                            style="width:320px;">
                                                                                            <!--<![endif]-->
                                                                                            <!--[if mso]><td class="t12" style="width:320;"><![endif]-->
                                                                                            <p class="t10"
                                                                                                style="margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:21px;font-weight:500;font-style:normal;font-size:16px;text-decoration:none;text-transform:none;direction:ltr;color:#111111;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px;">
                                                                                                To reset your password,
                                                                                                click the button below.
                                                                                                The link will
                                                                                                self-destruct after 30
                                                                                                minutes.</p>
                                                                                        </td>
                                                                                    </tr>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td>
                                                                                <div class="t15"
                                                                                    style="mso-line-height-rule:exactly;mso-line-height-alt:20px;line-height:20px;font-size:1px;display:block;">
                                                                                    &nbsp;</div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td>
                                                                                <!--[if !mso]>-->
                                                                                <table class="t17" role="presentation"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="Margin-left:auto;Margin-right:auto;">
                                                                                    <!--<![endif]-->
                                                                                    <!--[if mso]><table class="t17" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                                    <tr>
                                                                                        <!--[if !mso]>-->
                                                                                        <td class="t16"
                                                                                            style="background-color:#CDD6B0;overflow:hidden;width:286px;text-align:center;line-height:40px;mso-line-height-rule:exactly;mso-text-raise:8px;border-radius:12px 12px 12px 12px;">
                                                                                            <!--<![endif]-->
                                                                                            <!--[if mso]><td class="t16" style="background-color:#CDD6B0;overflow:hidden;width:286;text-align:center;line-height:40px;mso-line-height-rule:exactly;mso-text-raise:8px;border-radius:12px 12px 12px 12px;"><![endif]-->
                                                                                            <a href="{auth_service}/forgot-password?token={token}&email={email}">
                                                                                            <span class="t14"
                                                                                                style="display:block;margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:40px;font-weight:600;font-style:normal;font-size:14px;text-decoration:none;direction:ltr;color:#292929;text-align:center;mso-line-height-rule:exactly;mso-text-raise:8px;">
                                                                                                Reset your password</span>
                                                                                        </td>
                                                                                    </a>
                                                                                    </tr>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td>
                                                                                <div class="t20"
                                                                                    style="mso-line-height-rule:exactly;mso-line-height-alt:20px;line-height:20px;font-size:1px;display:block;">
                                                                                    &nbsp;</div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td>
                                                                                <!--[if !mso]>-->
                                                                                <table class="t22" role="presentation"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="Margin-left:auto;Margin-right:auto;">
                                                                                    <!--<![endif]-->
                                                                                    <!--[if mso]><table class="t22" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                                                    <tr>
                                                                                        <!--[if !mso]>-->
                                                                                        <td class="t21"
                                                                                            style="width:320px;">
                                                                                            <!--<![endif]-->
                                                                                            <!--[if mso]><td class="t21" style="width:320;"><![endif]-->
                                                                                            <p class="t19"
                                                                                                style="margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:21px;font-weight:500;font-style:normal;font-size:13px;text-decoration:none;text-transform:none;direction:ltr;color:#121212;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px;">
                                                                                                If you do not want to change your password or didn&#39;t request a reset, you can ignore and delete this email.
                                                                                            </p>
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
                                                        <div class="t26"
                                                            style="mso-line-height-rule:exactly;mso-line-height-alt:30px;line-height:30px;font-size:1px;display:block;">
                                                            &nbsp;</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <!--[if !mso]>-->
                                                        <table class="t28" role="presentation" cellpadding="0"
                                                            cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
                                                            <!--<![endif]-->
                                                            <!--[if mso]><table class="t28" role="presentation" cellpadding="0" cellspacing="0" align="center"><![endif]-->
                                                            <tr>
                                                                <!--[if !mso]>-->
                                                                <td class="t27"
                                                                    style="width:350px;padding:0 20px 0 20px;">
                                                                    <!--<![endif]-->
                                                                    <!--[if mso]><td class="t27" style="width:260;padding:0 20px 0 20px;"><![endif]-->
                                                                    <p class="t25"
                                                                        style="margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:16px;font-weight:500;font-style:normal;font-size:12px;text-decoration:none;text-transform:none;direction:ltr;color:#878787;text-align:center;mso-line-height-rule:exactly;mso-text-raise:1px;">
                                                                        <strong>{app_name}</strong> is a user-friendly platform designed to simplify 
                                                                        the analysis of RNA sequencing data, enabling researchers to easily identify
                                                                        genes that are differentially expressed between different biological conditions.</p>
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
                                <div class="t32"
                                    style="mso-line-height-rule:exactly;mso-line-height-alt:60px;line-height:60px;font-size:1px;display:block;">
                                    &nbsp;</div>
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

def get_text_body(app_name, auth_service, token, email):
    body_text = f"""
    Forgot your password?

    To reset your password, click the button below. The link will self-destruct after 30 minutes.

    Reset your password ( {auth_service}/forgot-password?token={token}&email={email} )

    If you do not want to change your password or didn't request a reset, you can ignore and delete this email.

    {app_name} is a user-friendly platform designed to simplify the analysis of RNA sequencing data, enabling researchers to easily identify genes that are differentially expressed between different biological conditions.
    """
    return body_text
