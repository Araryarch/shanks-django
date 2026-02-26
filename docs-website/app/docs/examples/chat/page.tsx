import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function ChatExamplePage() {
  return (
    <DocPage title="Real-time Chat" description="Build a real-time chat API with rooms, messages, and WebSocket support via Django Channels.">

      <Callout type="info" title="Requires Django Channels">
        Real-time features use Django Channels. Install with:{' '}
        <code>pip install channels channels-redis</code>
      </Callout>

      <h2>Setup</h2>
      <CodeBlock
        language="bash"
        code={`shanks new chat-api
cd chat-api
shanks create rooms --crud
shanks create messages --crud
shanks create auth --simple
pip install channels channels-redis
sorm db push
shanks run`}
      />

      <h2>Message Model</h2>
      <CodeBlock
        filename="entity/message.py"
        code={`from django.db import models

class Room(models.Model):
    name       = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'entity'

class Message(models.Model):
    room       = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author     = models.ForeignKey('entity.User', on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'entity'
        ordering  = ['created_at']`}
      />

      <h2>REST Endpoints</h2>
      <CodeBlock
        filename="internal/routes/chat.py"
        code={`from shanks import App, Response
from entity.message import Room, Message
from internal.middleware.auth import jwt_required

app = App()

@app.get('api/rooms')
def list_rooms(req):
    rooms = Room.find_many()
    return {'rooms': [{'id': r.id, 'name': r.name} for r in rooms]}

@app.get('api/rooms/<room_id>/messages', jwt_required)
def get_messages(req, room_id):
    msgs = Message.find_many(room_id=room_id)
    return {'messages': [{'author': m.author.username, 'content': m.content} for m in msgs[-50:]]}

@app.post('api/rooms/<room_id>/messages', jwt_required)
def send_message(req, room_id):
    msg = Message.create(room_id=room_id, author_id=req.user.id, content=req.body['content'])
    return Response().status_code(201).json({'id': msg.id})

router = app`}
      />

      <h2>API Endpoints</h2>
      <CodeBlock
        language="text"
        code={`GET  /api/rooms                  List all rooms
POST /api/rooms                  Create a room (JWT)
GET  /api/rooms/<id>/messages    Fetch last 50 messages (JWT)
POST /api/rooms/<id>/messages    Send a message (JWT)

WS   ws://localhost:8000/ws/chat/<room_name>/   WebSocket`}
      />
    </DocPage>
  );
}
