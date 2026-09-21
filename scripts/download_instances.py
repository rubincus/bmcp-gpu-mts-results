"""Fetch benchmark archives, verify published snapshot hashes, and extract only known instances."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--destination",type=Path,default=ROOT/"data/instances")
    ap.add_argument("--archives-dir",type=Path,help="Use already downloaded set1.zip and set2.zip, without network")
    a=ap.parse_args();a.destination.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/"data/instance_manifest.json").read_text())
    expected={r["name"]+".txt":r["sha256"] for r in manifest};seen=set()
    for source in json.loads((ROOT/"data/instance_archives.json").read_text()):
        if a.archives_dir:blob=(a.archives_dir/(source["name"]+".zip")).read_bytes()
        else:
            request=urllib.request.Request(source["url"],headers={"User-Agent":"BMCP-GPU-MTS-reproduction/0.1"})
            with urllib.request.urlopen(request,timeout=120) as response:blob=response.read()
        if sha(blob)!=source["sha256"]:raise ValueError(f"Archive hash changed: {source['name']}; no extraction performed")
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            for member in z.infolist():
                # Do not use extractall: flatten only allowlisted basenames.
                name=PurePosixPath(member.filename.replace("\\","/")).name
                # Set I omits the bmcp_ prefix; the manifest uses canonical IDs.
                if name not in expected and "bmcp_"+name in expected:
                    name="bmcp_"+name
                if name not in expected:continue
                data=z.read(member)
                if sha(data)!=expected[name]:raise ValueError(f"Instance mismatch: {name}")
                dest=a.destination/name
                if dest.exists() and sha(dest.read_bytes())!=expected[name]:raise ValueError(f"Refusing to replace modified file: {dest}")
                if not dest.exists():dest.write_bytes(data)
                seen.add(name)
    if seen!=set(expected):raise ValueError(f"Missing instances: {sorted(set(expected)-seen)}")
    print(f"Verified {len(seen)} instances in {a.destination}")
if __name__=="__main__":main()
