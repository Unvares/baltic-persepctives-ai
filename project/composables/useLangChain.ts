import { RemoteRunnable } from "@langchain/core/runnables/remote";
import { v4 as uuidv4 } from "uuid";

export const useLangChain = () => {
  const userId = uuidv4();
  useCookie("user_id").value = userId;

  const remoteChain = new RemoteRunnable({
    url: "https://langserve-14565.llm.mylab.th-luebeck.dev/openai/",
  });

  const invoke = async (params: Record<string, unknown>) => {
    const result = await remoteChain.invoke(params);
    return result;
  };

  return { invoke };
};
