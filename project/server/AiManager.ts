/*
 *
 * Example of how a mesage generation would look like using OpenAI API
 * with an API key define in .env of the root folder.
 * 
 * This component is responsible for communication with OpenAI API
 *
 */

import OpenAI from 'openai'
import type {Message} from '@/types';

const client = new OpenAI({
    apiKey: "Ligma"
});

export async function fetchResponse(requestMessages: Message[]): Promise<Message> {
    const response = await client.chat.completions.create({
        model: "gpt-3.5-turbo-1106",
        messages: requestMessages
    });

    if (response.choices) {
        return response.choices[0].message as Message;
    } else {
        throw new Error('AI could not send response.');
    }

}
