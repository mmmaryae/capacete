from bing_image_downloader import downloader

searches = {
    "helmet": [
        "worker wearing safety helmet",
        "construction worker helmet",
        "industrial worker safety helmet",
        "person wearing hard hat"
    ],
    "no_helmet": [
        "construction worker without helmet",
        "worker no hard hat",
        "industrial worker without safety helmet",
        "person at construction site without helmet"
    ]
}

LIMIT_PER_QUERY = 80
OUTPUT_DIR = "dataset_bruto"

for category, queries in searches.items():
    for query in queries:
        print(f"Baixando: {category} -> {query}")
        downloader.download(
            query,
            limit=LIMIT_PER_QUERY,
            output_dir=OUTPUT_DIR,
            adult_filter_off=True,
            force_replace=False,
            timeout=10,
            verbose=True
        )

print("Download finalizado.")

#Esse pacote baixa imagens do Bing por Python