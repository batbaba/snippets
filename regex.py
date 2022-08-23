def validate_contact_data(account_id, contact_data) -> dict:
    # Regex check if account id is 12 digits long
    pattern_account_id = re.compile("^\d{12}$")
    if not pattern_account_id.match(account_id):
        raise ValueError(f"Account ID {account_id} should be a 12 digit number")

    # Regex check if email is @persgroep.net or @dpgmedia.be
    pattern_email = re.compile("^[\w\.]+@persgroep.net$|^[\w\.]+@email.be$")
    if not pattern_email.match(contact_data["email"]):
        raise ValueError(
            f"Email {contact_data['email']} should be a @email.net or @email.be."
        )

    # Regex check if phone number starts with + and numbers or only numbers
    # If empty then set to "-", empty value is not allowed
    pattern_phone = re.compile("^\+\d+$|^\d+$")
    if not pattern_phone.match(contact_data["phone_number"]):
        if not contact_data["phone_number"]:
            contact_data["phone_number"] = "-"
        else:
            raise ValueError(
                "Phone number should be numeric or numeric and start with a +"
            )

    # If empty then set to "-", empty value is not allowed
    if not contact_data["title"]:
        contact_data["title"] = "-"
    if not contact_data["full_name"]:
        contact_data["full_name"] = "-"

    return contact_data
