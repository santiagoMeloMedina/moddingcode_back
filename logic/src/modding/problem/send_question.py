from typing import Any, Dict
from modding.common import http, logging
from modding.utils import email
from modding.common.aws_cli import AwsCustomClient as aws_client


_LOGGER = logging.Logger()

EMAIL_SUBJECT = "New message from student {username}"


@aws_client.ApiGateway.pre_handler
def handler(event: aws_client.ApiGateway.AGWEvent, context: Dict[str, Any]):
    try:
        result = _send_message_to_expert(
            **{**event.body, "user_email": event.get("headers", {}).get("username")}
        )

        response = http.get_response(http.HttpCodes.SUCCESS, body=result)
    except Exception as e:
        _LOGGER.error(e)
        response = http.get_standard_error_response()
    return response


def _send_message_to_expert(user_email: str, expert_email: str, message: str) -> None:
    ses_client = aws_client.ses(user_email)
    ses_client.send_html_email(
        email_address=expert_email,
        subject=EMAIL_SUBJECT.format(username=user_email),
        html_content=email.generate_message_email_html_template(message),
    )
    _LOGGER.info("Message sent from %s to %s" % (user_email, expert_email))
