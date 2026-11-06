"""Errores del dominio.

Son parte del lenguaje ubicuo: expresan reglas/condiciones del negocio,
no detalles técnicos de una librería concreta.
"""
from __future__ import annotations


class DomainError(Exception):
    """Base de todos los errores del dominio."""


class MasterPasswordProtected(DomainError):
    """El workspace usa una contraseña maestra: la clave fija no sirve.

    DBeaver (configuración de seguridad / versiones PRO) permite cifrar el
    almacén con una contraseña definida por el usuario. En ese caso el
    descifrado con la clave pública falla y hay que pedir la maestra.
    """

    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = workspace_path
        super().__init__(
            f"El workspace '{workspace_path}' parece protegido con contraseña maestra; "
            "la clave fija no puede descifrarlo."
        )


class CredentialsDecryptionError(DomainError):
    """No se pudo descifrar el archivo de credenciales por un motivo técnico."""


class CorruptCredentialsFile(DomainError):
    """El contenido descifrado no es un JSON de credenciales válido."""
