from base64 import b64encode, b64decode
from os import getenv
from random import randbytes
from subprocess import run
from hashlib import md5

def set_output(name, value):
    eof = b64encode(randbytes(16))
    with open(getenv("GITHUB_OUTPUT"), "a") as f:
        f.write(f"{name}<<{eof}{value}{eof}\n")

def curse_java_version():
    min_java = int(getenv("MIN_JAVA_VERSION"))
    max_java = int(getenv("MAX_JAVA_VERSION"))

    output = []
    for i in range(min_java, max_java+1):
        output.append(f"Java {i}") 
    return ",".join(output)

def curse_minecraft_version():
    patch_version = getenv("MC_VERSION")
    minor_version = ".".join(patch_version.split(".")[:-1])

set_output("curse_version", ",".join([
    curse_minecraft_version(),
    curse_java_version(),
    getenv("MOD_LOADER"),
    getenv("MOD_ENVIRONMENT")
]))

mod_file = getenv("MOD_FILE")
if getenv("JAR_SIGNING_STORE", ""):
    store = getenv("JAR_SIGNING_STORE")
    with open("keystore.jks", "w") as f:
        f.write(b64decode(store))
    alias = getenv("JAR_SIGNING_ALIAS")
    store_pass = getenv("JAR_SIGNING_STORE_PASS")
    key_pass = getenv("JAR_SIGNING_KEY_PASS")
    signed_jar = f"{'.'.join(mod_file.split['.'][:-1])}-sgd.jar"
    run(
        [
            "keytool", 
            "-genkey", 
            "-alias",
            alias, 
            "-keypass", 
            key_pass,
            "-storepass", 
            store_pass, 
            "-keystore", 
            "keystore.jks",
            "-signedjar",
            signed_jar,
            mod_file
        ]
    )
    mod_file = signed_jar
set_output("mod_file", mod_file)

digest = ""
with open(mod_file, "r") as f:
    file_hash = md5()
    while chunk := f.read(8192):
        file_hash.update(chunk)
    digest = file_hash.digest()

with open(f"{mod_file}.md5", "w") as f:
    f.write(digest)
set_output("md5_file", f"{mod_file}.md5")

changelog = getenv("CHANGELOG")
if getenv("INCLUDE_MD5_CHANGELOG") == "true":
    changelog += "\n\nMD5: {digest}\n"
set_output("changelog", changelog)