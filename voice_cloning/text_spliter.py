def split_text(input_text):
    
    chunk_size = 160
    chunks = []
    current_chunk = ""

    for word in input_text.split():
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "

    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


