import Chatbot from '@/components/chatbot/chatbot';

export default function ChatPage() {
  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 h-full">
        <Chatbot />
      </div>
    </div>
  );
}
