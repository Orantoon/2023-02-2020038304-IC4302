config = {
   "key_content": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCgpeY9g0zwRDgI
AIRwBnkI1lEI6UrAZLsSqDryxkdOvuts5d206sWEJSToODz5EjTQThikoq1FTJPJ
ASUHVQUbVDf3Q5hDuWPRqBrGP02B4pTyKk2HMmFIJfXZ3Nu7ImABFEIjTXMDQjcR
G9aMzXWlO8XYg/zUnQO1jBUvpaWQ1z9BlFYITLp1SUQw9lfxeD+g6lpjryAcgaX4
ROYGmw1BRVeyq96/5dyr1vv8CmOp3k0Wn27xx3l4z4NoAC+tMdo4GQab94o3DObs
d1A9Z4L0tq9+0TRux41M8WBPhuCe6QoryyDlCZhc4P86LSU1B3trKVh6eI27VPmb
uxEw8SkfAgMBAAECggEABs9BdTYNmtmpbl1nP8BmfQNop/ILoyAh9eZ/qS7ScvoQ
zKrpvPN+r91LNTS9EOm+p13IGaJzqc5XLVwJD8iA0Om+/ZI18Bj5rDdt+x1P0cOj
AKjeZG60RPSm+TctcT9BxonvS8PKrkauQuFlNM64v+pKtqTRoMmPELEBbOWeoQcN
jA/2io0vZ/EKnhLXqw3zqsnhCcbkh+BdSaMysJasd37rC4pzqAW3uBCNzGs/zUVl
YffsNSjOCeqKhPTxIyU4THkic35qTNkxBiH84SjDDWU1ItSGmHy0ajEv05M3XhtK
k71xBxRVLMFV4J0upuX/yKCXzOocH22YcdasdasdasdasQDLdAjn8lrRq0Ql2Y/B
a/GiDNp28gmpE5BTTAUx6PPd8IU6VM1lQIRIHiqMS4RA/f1U8IHIG18Oi4BddP3V
SJECfnqno5QYLguFLyFYskqSn3m167JgPwuiVNU7RhDJW11o3vAPecgtNtCKJvTc
0XcZmA21jOMdpXSym2ALsHfUXwKBgQDKI6kMLBY4rH1rGAyruedPLi7eIXrcs1ew
e+qGPlVwumn+i5+EJMK7pWx+toJt0etqG6yoByfM6TN2WkUQHCnVLE8I14CVrIfv
t4dzqNG5BuJumuR0/doPkDLQAIS/mNFrNCg4oMNUkC1Vv3KXQ56Cwe7Pk0hNeohg
BpaUC0zjQQKBgQDCsVCQfdixCh7VxaOOqfh6Zaht6OKbvNABFh9mipFMEo27q0k+
moW76bo3tVBjTWsu7FSVpLPLXG3DgWAiySWTaGuBnsTqeq2ljttvYHaCZz/2eg2h
ktNUTbAb38nSlq8F20mI1bZcpjbb7bmm0oARqvN7h84TIbFR9ePsa7vQKwKBgGL+
0+uCK9/Vmha40HvJr963X3yqKOGtc2SbS2AzZuSuZvqippyw5C3B9kCYYYgnJoPw
yb4Awx03mFx+GRSqtlIQQSSzZeXneSuNVmjuZMeY94vzj688I287z6bOmjS7QtSd
1pTlJsRjV9CG0jgChb7D+5DtMJvBRsjAcT5PyngBAoGBAJpeAo5FRp5fU7lLy4GL
Zb0Ncyawivm1AZeGH6gWcnE8ZECPJ5IyaiYWSiB7BrtRnG449GpfVogDbC3HkNU0
h/Bw3pFxlwRfyrClc5uJBW8IG7KyMa+lot+TT/l+EL8DiwRk/UVCpqQKI4GHDwDC
2qucf/+5HNIdrsnS1Xe7yxSF
-----END PRIVATE KEY-----""",
  "user": "ocid1.user.oc1..aaaaaaaahjsrlczdcqcazwhkb3jyotdwq4opnyxr5cx7ctxo3xd5uf7eu25q",
  "fingerprint": "cf:0d:bb:e3:e6:ee:b5:4c:9c:ea:10:ac:2d:e6:68:74",
  "tenancy": "ocid1.tenancy.oc1..aaaaaaaa22p5zz37ti2o4fo4wgid5iqaekkaxnykgycssznueu4kfz5272uq",
  "region": "us-chicago-1"
}

import oci
import io

oci.config.validate_config(config) # Validacion del config
object_storage = oci.object_storage.ObjectStorageClient(config) # Se conecta al Object Storage

bucket = 'nereo'
file = 'oc.py'

compartment_id = config['tenancy'] # Se crea el comparment_id a partir del tenancy id
namespace = object_storage.get_namespace().data # Se consigue el namespace del Object Storage

# Extraer del Object Storage
response = object_storage.get_object(namespace=compartment_id, bucket_name=bucket, object_name=file)
file_content = response.data.content
data = io.BytesIO(file_content.read())
print(data)

# Subir al Object Storage con Upload Manager
upload_manager = oci.object_storage.UploadManager(object_storage, max_parallel_uploads=10) # Max Parallel Uploads son las subidas que se pueden hacer al mismo tiempo
upload_manager.upload_file(namespace, bucket, file, file) # Se sube en un bucket, un archivo en el namespace

# key_content = API key?
# fingerprint = preguntar
# como se corre?