from django.http import JsonResponse
from flask import Flask
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import GPT2LMHeadModel, GPT2Tokenizer

from .models import ChatMessage

app = Flask(__name__)
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2',
                                          pad_token='chat')


@api_view(['POST'])
def send_message(request):
    """
    Endpoint to handle sending messages from the user and generating bot responses.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Response: A JSON response containing the generated bot message.
    """
    response = Response({'key': 'value'})

    # Allow requests from the specified origin with credentials
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response['Access-Control-Allow-Credentials'] = 'true'

    user_message = request.data.get('message', '')
    bot_message = generate_text(user_message)

    session_id = request.session.session_key
    if session_id is None:
        request.session.save()
        session_id = request.session.session_key

    # Save the user's message in the database
    ChatMessage.objects.create(text=user_message, sender='user', session_id=session_id)
    # Save the bot's response in the database
    ChatMessage.objects.create(text=bot_message, sender='bot', session_id=session_id)

    return Response({'message': bot_message})


def generate_text(user_message):
    input_ids = tokenizer.encode(user_message, return_tensors='pt')

    if input_ids is None or input_ids.numel() == 0:
        return "Unable to generate response. Input is empty."

    if tokenizer.pad_token_id is None or tokenizer.pad_token_id == tokenizer.eos_token_id:
        return "Tokenizer's pad_token_id is not set or is set to eos_token_id."

    attention_mask = input_ids.ne(tokenizer.pad_token_id).float()

    # Specify attention_mask and pad_token_id in the generate function
    output = model.generate(
        input_ids,
        max_length=100,
        attention_mask=attention_mask,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_k=50,
        temperature=0.7,
        do_sample=False,
    )

    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded_output


@api_view(['GET'])
def get_user_messages(request):
    """
    Endpoint to retrieve user messages stored in the database.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - JsonResponse: A JSON response containing the user's messages.
    """
    session_id = request.session.session_key

    if session_id is None:
        return Response({'user_messages': []})

    user_messages = ChatMessage.objects.filter(session_id=session_id).values('text', 'sender')

    return JsonResponse({'user_messages': list(user_messages)})
