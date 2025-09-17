class EmailValueObject():
    def __init__(
            self,
            subject: str,
            template_path: str,
            template_variables: dict,
            to: list[str]
    ):
        self.subject = subject
        self.template_path = template_path
        self.template_variables = template_variables
        self.to = to
