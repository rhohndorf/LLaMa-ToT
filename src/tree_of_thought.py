from llama_cpp import Llama
import config as cfg
import templates as tpl
    
llm = Llama(cfg.model_path, n_ctx=2048)

def ask(prompt):
    response = llm(prompt, stop=["[Input]"], temperature=cfg.temperature, top_k=50)
    return response['choices'][0]['text'].rstrip().lstrip()


def solve(goal, plan):
    """Find a plan with DFS"""
    planner_prompt = tpl.make_planner_prompt(goal, plan)
    print(planner_prompt)
    options = [ask(planner_prompt) for i in range(cfg.branching_factor)]
    while len(options) > 0:
        critic_prompt = tpl.make_critic_prompt(goal, plan, options)
        print(critic_prompt)
        chosen_option = options.pop(int(ask(critic_prompt)) -1)

        # Termination criterion 1: Solution found. The plan is complete and can be returned 
        if chosen_option == "DONE":
            return plan

        # Termination criterion 2: Max plan length reached and no valid plan found. Backtrack 1 step.
        if len(plan) == cfg.max_plan_length:
            return None
        
        # Explore subtree
        return solve(goal, plan+[{'task':chosen_option, 'state':None}]) 


if __name__ == "__main__":
    # goal = "solve for x,y and z in the following system of equations x=17z + 3; y=2x; z=1"
    goal = "write a short story about aliens"
    # goal = "Combine the numbers 4,9,10 and 13 with the basic arithmatic operations(+,-,*,/) to obtain the result 24"
    plan = None

    while plan == None:
        plan = solve(goal, [])

    print(plan)