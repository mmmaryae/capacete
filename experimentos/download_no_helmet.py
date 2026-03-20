from bing_image_downloader import downloader

queries = [
    "person portrait",
    "person face photo",
    "people portrait photo",
    "man portrait",
    "woman portrait",
    "person looking at camera",
    "people standing portrait",
    "person headshot photo",
    "worker without helmet",
    "worker without safety helmet",
    "construction worker without hard hat",
    "construction site worker no helmet",
    "industrial worker without helmet",
    "builder without helmet"
]

LIMIT = 80

for query in queries:
    print(f"\nBaixando: {query}\n")

    downloader.download(
        query,
        limit=LIMIT,
        output_dir="dataset_download",
        adult_filter_off=True,
        force_replace=False,
        timeout=60,
        verbose=True
    )

print("\nDownload finalizado.\n")