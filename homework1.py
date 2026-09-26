from collections import Counter
import csv
import re

filtered_tweets = []

with open("IRAhandle_tweets_1.csv", "r", encoding="utf-8") as input_file:
    reader = csv.DictReader(input_file)

    for index, row in enumerate(reader):
        if index == 10000:
            break

        if row["language"] == "English" and "?" not in row["content"]:
            filtered_tweets.append(row)

trump_pattern = r"(?<![A-Za-z0-9])Trump(?![A-Za-z0-9])"

for row in filtered_tweets:
    if re.search(trump_pattern, row["content"]):
        row["trump_mention"] = "T"
    else:
        row["trump_mention"] = "F"
output_columns = ["tweet_id", "publish_date", "content", "trump_mention"]

with open("dataset.tsv", "w", encoding="utf-8", newline="") as output_file:
    writer = csv.DictWriter(
        output_file,
        fieldnames=output_columns,
        delimiter="\t"
    )

    writer.writeheader()

    for row in filtered_tweets:
        output_row = {
            column: row[column]
            for column in output_columns
        }
        writer.writerow(output_row)       
print("Number of filtered tweets:", len(filtered_tweets))
print("First annotation:", filtered_tweets[0]["trump_mention"])

trump_count = sum(
    row["trump_mention"] == "T"
    for row in filtered_tweets
)

fraction = trump_count / len(filtered_tweets)

truncated_integer = (
    trump_count * 1000
) // len(filtered_tweets)

truncated_fraction = f"{truncated_integer / 1000:.3f}"

with open("results.tsv", "w", encoding="utf-8", newline="") as results_file:
    writer = csv.writer(results_file, delimiter="\t")
    writer.writerow(["result", "value"])
    writer.writerow(["frac-trump-mentions", truncated_fraction])

print("Number of Trump mentions:", trump_count)
print("Exact fraction:", fraction)
print("Truncated fraction:", truncated_fraction)

tweet_id_counts = Counter(
    row["tweet_id"]
    for row in filtered_tweets
)

duplicate_ids = {
    tweet_id: count
    for tweet_id, count in tweet_id_counts.items()
    if count > 1
}

extra_rows = sum(
    count - 1
    for count in duplicate_ids.values()
)

print("Number of duplicated tweet IDs:", len(duplicate_ids))
print("Number of extra repeated rows:", extra_rows)

print("\nExamples of duplicated tweets:")

shown = 0

for tweet_id, count in duplicate_ids.items():
    print("Tweet ID:", tweet_id)
    print("Occurrences:", count)

    for row in filtered_tweets:
        if row["tweet_id"] == tweet_id:
            print("Content:", row["content"])

    print()

    shown += 1

    if shown == 3:
        break

content_counts = Counter(
    row["content"]
    for row in filtered_tweets
)

duplicate_contents = {
    content: count
    for content, count in content_counts.items()
    if count > 1
}

extra_content_rows = sum(
    count - 1
    for count in duplicate_contents.values()
)

print("\nNumber of duplicated contents:", len(duplicate_contents))
print("Number of extra rows from repeated content:", extra_content_rows)

print("\nExamples of repeated content:")

shown = 0

for content, count in duplicate_contents.items():
    print("Occurrences:", count)
    print("Content:", content)

    for row in filtered_tweets:
        if row["content"] == content:
            print(
                "Tweet ID:", row["tweet_id"],
                "| Author:", row["author"],
                "| Retweet:", row["retweet"]
            )

    print()

    shown += 1

    if shown == 5:
        break    