from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def send_otp_email(email, otp, purpose="verify"):

    company_name = "xyzcombo"

    company_logo = (
        "https://xyzcombo.com/static/logo.png"
    )

    support_email = settings.DEFAULT_FROM_EMAIL

    if purpose == "reset":
        subject = "Reset Your Password"
        heading = "Password Reset Request"
        sub_heading = (
            "Use the OTP below to reset your password securely."
        )
        button_text = "Reset Password"
    else:
        subject = "Verify Your Account"
        heading = "Account Verification"
        sub_heading = (
            "Use the OTP below to verify your account securely."
        )
        button_text = "Verify Account"

    # ==========================================
    # TEXT VERSION
    # ==========================================

    text_content = f"""
{heading}

Your OTP Code: {otp}

This OTP is valid for 5 minutes.

If you did not request this email,
please ignore it.

Thanks,
{company_name}
"""

    # ==========================================
    # HTML EMAIL TEMPLATE
    # ==========================================

    html_content = f"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
</head>

<body style="
    margin:0;
    padding:0;
    background:#f4f7fb;
    font-family:Arial,sans-serif;
">

<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td align="center" style="padding:40px 15px;">

    <!-- MAIN CARD -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0"
        style="
            max-width:600px;
            background:#ffffff;
            border-radius:16px;
            overflow:hidden;
            box-shadow:0 8px 24px rgba(0,0,0,0.08);
        ">

        <!-- HEADER -->
        <tr>
            <td style="
                background:linear-gradient(135deg,#111827,#1f2937);
                padding:35px 20px;
                text-align:center;
            ">

                <img 
                    src="{company_logo}" 
                    alt="{company_name}"
                    width="70"
                    style="
                        margin-bottom:15px;
                        border-radius:12px;
                    "
                >

                <h1 style="
                    margin:0;
                    color:#ffffff;
                    font-size:28px;
                    font-weight:700;
                    letter-spacing:1px;
                ">
                    {company_name}
                </h1>

            </td>
        </tr>

        <!-- BODY -->
        <tr>
            <td style="padding:45px 35px;">

                <!-- ICON -->
                <div style="text-align:center; margin-bottom:20px;">

                    <div style="
                        width:80px;
                        height:80px;
                        background:#eef2ff;
                        border-radius:50%;
                        margin:auto;
                        line-height:80px;
                        font-size:36px;
                    ">
                        🔐
                    </div>

                </div>

                <!-- HEADING -->
                <h2 style="
                    margin-top:0;
                    margin-bottom:15px;
                    color:#111827;
                    text-align:center;
                    font-size:28px;
                ">
                    {heading}
                </h2>

                <!-- SUB HEADING -->
                <p style="
                    color:#6b7280;
                    text-align:center;
                    font-size:16px;
                    line-height:28px;
                    margin-bottom:35px;
                ">
                    {sub_heading}
                </p>

                <!-- OTP BOX -->
                <div style="text-align:center; margin:40px 0;">

                    <div style="
                        display:inline-block;
                        background:#f9fafb;
                        border:2px dashed #6366f1;
                        border-radius:14px;
                        padding:20px 40px;
                        font-size:38px;
                        font-weight:700;
                        letter-spacing:10px;
                        color:#111827;
                    ">
                        {otp}
                    </div>

                </div>

                <!-- VALIDITY -->
                <p style="
                    text-align:center;
                    color:#6b7280;
                    font-size:15px;
                    margin-bottom:35px;
                ">
                    This OTP will expire in
                    <strong>5 minutes</strong>.
                </p>

                <!-- BUTTON -->
                <div style="text-align:center; margin-bottom:35px;">

                    <a href="#"
                        style="
                            display:inline-block;
                            background:#4f46e5;
                            color:#ffffff;
                            text-decoration:none;
                            padding:14px 32px;
                            border-radius:10px;
                            font-size:16px;
                            font-weight:600;
                        ">
                        {button_text}
                    </a>

                </div>

                <!-- WARNING -->
                <div style="
                    background:#fff7ed;
                    border-left:4px solid #f97316;
                    padding:16px;
                    border-radius:8px;
                ">

                    <p style="
                        margin:0;
                        color:#9a3412;
                        font-size:14px;
                        line-height:24px;
                    ">
                        If you did not request this email,
                        you can safely ignore it.
                    </p>

                </div>

            </td>
        </tr>

        <!-- FOOTER -->
        <tr>
            <td style="
                background:#f9fafb;
                padding:30px;
                text-align:center;
                border-top:1px solid #e5e7eb;
            ">

                <p style="
                    margin:0 0 10px;
                    color:#6b7280;
                    font-size:14px;
                ">
                    Need help? Contact our support team.
                </p>

                <p style="
                    margin:0 0 15px;
                    color:#111827;
                    font-size:14px;
                    font-weight:600;
                ">
                    📧 {support_email}
                </p>

                <p style="
                    margin:0;
                    color:#9ca3af;
                    font-size:12px;
                ">
                    © 2026 {company_name}. All rights reserved.
                </p>

            </td>
        </tr>

    </table>

</td>
</tr>
</table>

</body>
</html>
"""

    try:

        email_message = EmailMultiAlternatives(
            subject=subject,
            body=strip_tags(text_content),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        email_message.attach_alternative(
            html_content,
            "text/html"
        )

        email_message.send(fail_silently=False)

        return True

    except Exception as e:

        logger.error(
            f"OTP email failed for {email}: {str(e)}"
        )

        return False