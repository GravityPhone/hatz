import openai
from typing_extensions import override
import time

class AssistantManager:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key
        self.client = openai

    def create_thread(self):
        try:
            thread = self.client.beta.threads.create()
            print(f'Successfully created thread with ID: {thread.id}')
            return thread.id
        except Exception as e:
            print(f"Failed to create a thread: {e}")
            return None

    def add_message_to_thread(self, thread_id, message_content, role="user"):
        try:
            message = self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role=role,
                content=message_content
            )
            print(f'Successfully added the message with ID: {message.id} to thread: {thread_id}')
            return message.id
        except Exception as e:
            print(f"Failed to add message to thread {thread_id}: {e}")
            return None

    def run_assistant(self, thread_id, assistant_id, instructions):
      try:
          with self.client.beta.threads.runs.create_and_stream(
              thread_id=thread_id,
              assistant_id=assistant_id,
              instructions=instructions,
              event_handler=EventHandler(),
          ) as stream:
              stream.until_done()
          print(f'Successfully started the assistant on thread: {thread_id}')
          return True
      except Exception as e:
          print(f"Failed to run assistant on thread {thread_id}: {e}")
          return False

    

    def retrieve_most_recent_message(self, thread_id):
        try:
            response = self.client.beta.threads.messages.list(thread_id=thread_id, order='desc', limit=1)
            # Assuming response.data contains the messages and taking the first one
            recent_message = response.data[0] if response.data else None
            if recent_message:
                print(f'Retrieved the most recent message: {recent_message.id} from thread: {thread_id}')
            return recent_message
        except Exception as e:
            print(f"Failed to retrieve the most recent message from thread {thread_id}: {e}")
            return None
