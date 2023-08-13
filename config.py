from Cryptodome.Cipher import AES
class Config:
    # Block structure: KEY || DATA
    KEY_SIZE = 16
    BLOCK_SIZE = 32
    LOCAL_MEMORY_SIZE = 120
    BIN_SIZE = int(LOCAL_MEMORY_SIZE/2)
    CIPHER_KEY = b'Sixteen byte key'
    CIPHER = AES.new(CIPHER_KEY, AES.MODE_ECB, use_aesni=True)