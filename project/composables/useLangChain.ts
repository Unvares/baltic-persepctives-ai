import { RemoteRunnable } from "@langchain/core/runnables/remote";
import { v4 as uuidv4 } from "uuid";

export const useLangChain = () => {
  const userId = uuidv4();
  useCookie("user_id").value = userId;

  const remoteChain = new RemoteRunnable({
    url: "http://localhost:8080/openai/",
  });

  const invoke = async (params: Record<string, unknown>) => {
    const result = await remoteChain.invoke(params, {
      configurable: {
        user_id: userId,
        conversation_id: "1",
      },
    });
    return result;
  };

  return { invoke };
};
