import { fetchResponse } from '~/server/AiManager';
import type { Message } from '@/types';
import { readBody } from 'h3';


export default defineEventHandler(async (event) => {
    try {
        const requestMessages: Message[] = await readBody(event);
        const responseMessage = await fetchResponse(requestMessages);
        return responseMessage;
    } catch (error) {
        event.res.statusCode = 500;
        return { error: 'Failed to fetch response from OpenAI' };
    }
});
