class GerenciarArquivosException(Exception):
    """Exceção personalizada que retorna uma mensagem padrão caso nenhuma seja fornecida."""

    def __init__(self, exception_message=None):
        """
        Inicializa a exceção com uma mensagem personalizada ou uma mensagem padrão.

        Args:
            exception_message (str, optional): Mensagem de erro personalizada.
                Se None, será usada a mensagem padrão. Defaults to None.
        """
        self.exception_message = exception_message if exception_message is not None else "Erro default"
        super().__init__(self.exception_message)

    def __str__(self):
        """Retorna a mensagem de exceção."""
        return self.exception_message
