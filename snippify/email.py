from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = "snippify/activation.html"


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "snippify/confirmation.html"


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "snippify/password_reset.html"


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "snippify/password_changed_confirmation.html"
