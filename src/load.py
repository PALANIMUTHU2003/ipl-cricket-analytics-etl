import pandas as pd

from config import OUTPUT_PATH


def save_csv(data, filename):

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(data)

    output_file = OUTPUT_PATH / filename

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")