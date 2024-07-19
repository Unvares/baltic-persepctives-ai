import OpenAI from 'openai'
import type {Message} from '@/types';

const openai = new OpenAI({
  apiKey: "sk-proj-AdIuNRsaRBF521qXqYoST3BlbkFJBxgJ7H7mTT8u3uN9xmG5"
});

export async function fetchResponse(requestMessages: Message[]): Promise<Message> {
    const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: requestMessages
    });

    if (response.choices) {
        return response.choices[0].message as Message;
    } else {
        throw new Error('AI could not send response.');
    }

}
