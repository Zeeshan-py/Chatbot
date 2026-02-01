import { streamText, tool } from 'ai';
import { groq } from '@ai-sdk/groq';
import { z } from 'zod';

const model = groq('mixtral-8x7b-32768');

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model,
    system: `You are FRIDAY, an advanced AI agent in an intelligent control center. You are sophisticated, intelligent, and capable of breaking down complex tasks into executable steps. 
    
    When a user asks you to do something, analyze the goal deeply and provide a comprehensive action plan with specific steps. Be confident, technical, and precise. You can use tools to help execute tasks.`,
    messages,
    tools: {
      analyzePlan: tool({
        description: 'Break down a goal into specific executable steps',
        inputSchema: z.object({
          goal: z.string(),
          steps: z.array(z.string()),
          priority: z.enum(['critical', 'high', 'medium', 'low']),
        }),
        execute: async ({ goal, steps, priority }) => {
          return {
            success: true,
            analysis: `Analyzed goal: ${goal}`,
            stepCount: steps.length,
            estimatedComplexity: steps.length > 5 ? 'complex' : 'moderate',
            priority,
          };
        },
      }),
      executeTask: tool({
        description: 'Execute a specific task with given parameters',
        inputSchema: z.object({
          task: z.string(),
          parameters: z.record(z.string()),
        }),
        execute: async ({ task, parameters }) => {
          return {
            taskId: `TASK_${Date.now()}`,
            status: 'executing',
            task,
            parameters,
          };
        },
      }),
      querySystem: tool({
        description: 'Query system status and permissions',
        inputSchema: z.object({
          query: z.string(),
        }),
        execute: async ({ query }) => {
          return {
            query,
            systemStatus: 'online',
            permissions: ['execute', 'analyze', 'monitor'],
            resources: { cpu: '45%', memory: '62%', network: 'stable' },
          };
        },
      }),
    },
  });

  return result.toUIMessageStreamResponse();
}
