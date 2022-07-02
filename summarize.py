'''
This program is for summarizing large amounts of text using GPT-3.

It takes a filename on the command line and reads the text from that file.

Then it allows the user to interactively summarize the text.
'''

import setcreds
import openai
import sys

C_CHUNK_SIZE = 1000 # number of words we can summarize in one go

def summarize(lines):
    # first construct the prompt for GPT-3
    prompt = [
        "Part of a transcript of a video consists of the following:",
        "---"
    ]



    prompt.extend(lines)

    prompt.extend([
        "---",
        "",
        "Present a short summary of the informational content of the part of the transcript.",
    ])

    prompt_text = "\n".join(prompt)

    # get the summary from GPT-3
    completion = openai.Completion.create(
        engine="davinci", 
        max_tokens=200, 
        temperature=0.1,
        prompt=prompt_text,
        frequency_penalty=1
    )

    summary_raw_text = completion.choices[0].text

    # print(f"Summary raw text: {summary_raw_text}")

    summary_raw_lines = summary_raw_text.split("\n")

    if "---" in summary_raw_text:
        # remove all lines until the first "---", and after the last "---",
        # and also remove the "---" lines
        inside_summary = False
        summary_lines = []
        for line in summary_raw_lines:
            line = line.strip()
            if inside_summary:
                if line == "---":
                    break
                else:
                    summary_lines.append(line)
            else:
                if line == "---":
                    inside_summary = True
    elif "\n" in summary_raw_text:
        summary_lines = summary_raw_text.split("\n")

        # remove all leading empty lines (stripped)
        while summary_lines[0].strip() == "":
            summary_lines = summary_lines[1:]

        # remove all lines after the first empty line (stripped)
        summary_lines_copy = summary_lines[:]
        summary_lines = []
        for line in summary_lines_copy:
            if line.strip() == "":
                break
            else:
                summary_lines.append(line)
    else:
        # keep all lines
        summary_lines = summary_raw_text.split("\n")

    # join the lines into a single string
    summary = "\n".join(summary_lines)

    return summary

def summarize_the_summaries(summaries):
    '''
    summaries is a list of strings, each of which is a summary.
    '''

    prompt = []

    # add blank lines after each summary
    for index, summary in enumerate(summaries):
        prompt.extend([
            f"A summary of part {index + 1} of the transcript is:", 
            "---",
            summary,
            "---",
            "",
        ])
    
    prompt.append("Present a short summary of the informational content of the all the summaries")

    prompt_text = "\n".join(prompt)

    # get the summary from GPT-3
    completion = openai.Completion.create(
        engine="davinci", 
        max_tokens=300, 
        temperature=0.1,
        prompt=prompt_text,
        frequency_penalty=1
    )

    summary_raw_text = completion.choices[0].text

    print(f"Summary raw text: {summary_raw_text}")

    summary_raw_lines = summary_raw_text.split("\n")

    # remove all lines until the first "---", and after the last "---",
    # and also remove the "---" lines
    inside_summary = False
    summary_lines = []
    for line in summary_raw_lines:
        line = line.strip()
        if inside_summary:
            if line == "---":
                break
            else:
                summary_lines.append(line)
        else:
            if line == "---":
                inside_summary = True

    # join the lines into a single string
    summary = "\n".join(summary_lines)

    return summary

def summarize_the_topics(topics_list):

    prompt = [
        "Question:",
        "A rough list of topics from a video transcript is as follows:"
    ]

    prompt.extend(topics_list)

    prompt.extend([
        "",
        "Given the above, present a short summary of what the video transcript is about.",
        "Answer:"
    ])
    #     "Your task is clean up this list of topics.",
    #     "It should be presented cleanly as bullet points (use hyphens).",
    #     "Each bullet point should be on its own line.",
    #     "Each bullet point should only be a few words long, or a short sentence.",
    #     "Don't include duplicate topics."
    #     "",
    #     "Please present your rewritten list of topics. Remember that each line must be a separate bullet point.",
    #     "Answer:"
    # ])
    prompt_text = "\n".join(prompt)

    # print (f"Prompt text: {prompt_text}")

    # get the summary from GPT-3
    completion = openai.Completion.create(
        engine="davinci", 
        max_tokens=300, 
        temperature=0.1,
        prompt=prompt_text,
        frequency_penalty=1
    )

    summary_raw_text = completion.choices[0].text

    # print(f"Topics raw text: {summary_raw_text}")

    summary_raw_lines = summary_raw_text.split("\n")

    # remove all blank lines
    summary_lines = []
    for line in summary_raw_lines:
        line = line.strip()
        if line != "":
            summary_lines.append(line)

    # join the lines into a single string
    summary = "\n".join(summary_lines)

    return summary

def get_topics(lines):
    # first construct the prompt for GPT-3
    prompt = [
        "Part of a transcript of a video consists of the following:",
        "---"
    ]

    prompt.extend(lines)

    prompt.extend([
        "---",
        "",
        "What are the important topics mentioned?",
        "A topic should only be a few words long, or a short sentence.",
        "Topics:"
    ])

    prompt_text = "\n".join(prompt)

    # get the summary from GPT-3
    bad = True
    tries_remaining = 3
    while bad and tries_remaining > 0:
        print(f"Tries remaining: {tries_remaining}")

        completion = openai.Completion.create(
            engine="davinci", 
            max_tokens=200, 
            temperature=(3 - tries_remaining) * 0.1,
            prompt=prompt_text,
            frequency_penalty=1
        )

        raw_text = completion.choices[0].text

        if "Part of a transcript of" in raw_text:
            bad = True
            tries_remaining -= 1
        
        elif "Present a short list" in raw_text:
            bad = True
            tries_remaining -= 1
        
        else:
            bad = False
            break

    if bad:
        return ""

    # print(f"raw text: {raw_text}")

    raw_lines = raw_text.split("\n")

    if "---" in raw_text:
        # remove all lines until the first "---", and after the last "---",
        # and also remove the "---" lines
        inside_summary = False
        summary_lines = []
        for line in raw_lines:
            line = line.strip()
            if inside_summary:
                if line == "---":
                    break
                else:
                    summary_lines.append(line)
            else:
                if line == "---":
                    inside_summary = True
    elif "\n" in raw_text:
        summary_lines = raw_text.split("\n")

        # remove all leading empty lines (stripped)
        while summary_lines[0].strip() == "":
            summary_lines = summary_lines[1:]

        # remove all lines after the first empty line (stripped)
        summary_lines_copy = summary_lines[:]
        summary_lines = []
        for line in summary_lines_copy:
            if line.strip() == "":
                break
            else:
                summary_lines.append(line)
    else:
        # keep all lines
        summary_lines = raw_text.split("\n")

    # join the lines into a single string
    summary = "\n".join(summary_lines)

    return summary

def calc_stats(text):
    # break the text into lines
    lines = text.split("\n")

    # number of lines in the text
    num_lines = len(lines)

    # number of words in the text
    num_words = 0
    for line in lines:
        num_words += len(line.split())

    # number of characters in the text
    num_chars = len(text)

    # number of paragraphs in the text
    num_paragraphs = 0
    for line in lines:
        if line == "":
            num_paragraphs += 1
    
    # number of chunks in the text
    # round up to the nearest chunk
    num_chunks = (num_words + C_CHUNK_SIZE - 1) // C_CHUNK_SIZE

    # return a string with the stats
    stats_lines = [
        "Number of lines: {}".format(num_lines),
        "Number of words: {}".format(num_words),
        "Number of characters: {}".format(num_chars),
        "Number of paragraphs: {}".format(num_paragraphs),
        "Number of chunks: {}".format(num_chunks),
    ]


    return "\n".join(stats_lines)

def get_chunks(text):
    '''
    return a list of lists of strings.
    Each list of strings in a list of lines, or equivalently a chunk.
    We make sure each chunk is as long as possible, 
    but less than C_CHUNK_SIZE words.
    '''
    # break the text into lines
    lines = text.split("\n")

    # list of chunks
    chunks = []

    current_chunk = []
    current_chunk_len_in_words = 0

    for line in lines:
        # split the line into words
        words = line.split()

        current_line_len_in_words = len(words)

        # if the current chunk is too long, add it to the list of chunks
        if current_chunk_len_in_words + current_line_len_in_words > C_CHUNK_SIZE:
            chunks.append(current_chunk)
            current_chunk = []
            current_chunk_len_in_words = 0

        # add the words to the current chunk
        current_chunk.append(line)
        current_chunk_len_in_words += current_line_len_in_words
    
    # add the last chunk to the list of chunks
    chunks.append(current_chunk)

    return chunks

def main():

    if len(sys.argv) != 2:
        print("Usage: summarize.py <filename>")
        return

    # get the filename from the command line
    filename = sys.argv[1]

    # read the text from the file
    with open(filename, "r") as f:
        text = f.read()

    print("Welcome to the GPT-3 Summarizer!")
    print("Commands: 'q' to quit, 's' to summarize, 't' to get topics covered, 'p' to get people mentioned, 'z' to get stats")
    print("")

    # now we sit in a loop getting user commands
    while True:
        # get a line of text from the user
        try:
            line = input(">>> ")
        except EOFError:
            break

        # if the user wants to quit, we're done
        if line == "q":
            break

        # if the user wants to summarize, do it
        if line == "s":
            chunks = get_chunks(text)

            # get a summary of each chunk
            summaries = []
            for index, chunk in enumerate(chunks):
                summary = summarize(chunk)
                # print(f"Chunk {index+1} of {len(chunks)}:")
                # print(chunk)
                # print("")
                print(f"Summary:")
                print(summary)
                print("")

                summaries.append(summary)

            # get a summary of the summaries
            summary = summarize_the_summaries(summaries)
            print("Summary of the summaries:")
            print(summary)
            print("")

        # if the user wants to get the topics covered, do it
        if line == "t":
            chunks = get_chunks(text)

            # get a summary of each chunk
            topics_per_chunk = []
            for index, chunk in enumerate(chunks):
                topics = get_topics(chunk)
                # print(f"Chunk {index+1} of {len(chunks)}:")
                # print(chunk)
                # print("")
                print(f"Topics {index+1}:")
                print(topics)
                print("")

                topics_per_chunk.append(topics)

            # get a summary of topics
            topics_summary =  summarize_the_topics(topics_per_chunk)
            print("Summary based on topics:")
            print(topics_summary)
            print("")

            topics_summary_lines = topics_summary.split("\n")
            final_topics = get_topics(topics_summary_lines)
            print("Final topics:")
            print(final_topics)
            print("")




        # if the user wants to see stats, do it
        if line == "z":
            stats = calc_stats(text)

            # print the stats
            print("")
            print(stats)
            print("")

    print("Goodbye!")

# call main() if this is the main module
if __name__ == "__main__":
    main()
