import { RemoteRunnable } from "@langchain/core/runnables/remote";

export const useLangChain = () => {
  const remoteChain = new RemoteRunnable({
    url: "https://langserve-14565.llm.mylab.th-luebeck.dev/openai/",
  });

  const invoke = async (params: Record<string, string>) => {
    const result = await remoteChain.invoke(params);
    return result;
  };

  return { invoke };
};
