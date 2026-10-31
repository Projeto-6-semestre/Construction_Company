import Image from "next/image";
import type { ChatMessage } from "@/types/api";
import styles from "./ChatMessageBubble.module.css";

export function ChatMessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  return (
    <div className={`${styles.row} ${isUser ? styles.rowUser : styles.rowAssistant}`}>
      {!isUser && (
        <Image
          src="/images/avatar-1.jpg"
          alt="Avatar do agente"
          width={32}
          height={32}
          className={styles.avatar}
        />
      )}
      <div className={`${styles.bubble} ${isUser ? styles.bubbleUser : styles.bubbleAssistant}`}>
        {message.content}
      </div>
      {isUser && (
        <Image
          src="/images/avatar-2.jpg"
          alt="Avatar do usuario"
          width={32}
          height={32}
          className={styles.avatar}
        />
      )}
    </div>
  );
}
