conversation_history = {}

def trim_history(history, max_length=16384):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history

def clear_command(user_id, user_name):
    conversation_history[user_id] = []
    print(f"{user_name}({user_id}) очистил диалог.")
    message = "История диалога успешно очищена."
    return message
