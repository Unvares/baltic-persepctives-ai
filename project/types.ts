type ChatHistory = [Message];

type Message = {
    role: "system" | "user" | "assistant" ;
    content: string;
}

export type {ChatHistory, Message};
