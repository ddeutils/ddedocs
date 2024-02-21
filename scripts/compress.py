from pathlib import Path
import gzip


main_path: Path = Path(__file__).parent.parent
asset_path: Path = main_path / "assets" / "books"
backup_path: Path = main_path / "backup" / "books"


def main():
    asset_path.mkdir(exist_ok=True)
    backup_path.mkdir(exist_ok=True)

    if asset_path.exists():
        print("Start Searching file for compress to gzip format ...")

        for file in asset_path.rglob("*.pdf"):
            if ".gz." not in file.name:
                print(f"Compress: {file.name}")
                with gzip.open(f"{file}.gz", mode="wb") as f:
                    f.writelines(file.open(mode="rb"))
                file.rename(backup_path / file.name)


if __name__ == "__main__":
    main()
