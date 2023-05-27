from string import Template

executer = Template("""
[Input] What year is it?
[Output] We are in [[DATE_YEAR]].
[Input] Please tell me the largest city in Europe.
[Output] The largest city in Europe is Moscow, the capital of Russia.
[Input] What can you tell me about Moscow?
[Output] Moscow, on the Moskva River in western Russia, is the nation's cosmopolitan capital. In its historic core is the Kremlin, a complex that's home to the president and tsarist treasures in the Armoury. Outside its walls is Red Square, Russia’s symbolic center.
[Input] What is a cat?
[Output] A cat is a domestic species of small carnivorous mammal. It is the only domesticated species in the family Felidae.
[Input] How do I pass command line arguments to a Node.js program?
[Output] The arguments are stored in process.argv.

    argv[0] is the path to the Node. js executable.
    argv[1] is the path to the script file.
    argv[2] is the first argument passed to the script.
    argv[3] is the second argument passed to the script and so on.
[Input] Name a color.
[Output] Blue.
[Input] What time is it?
[Output] It is [[DATE_TIME]].
[Input]
With the goal to $goal in mind, work on the following task:
$task
[Output]
""")

critic = Template("""
[Input]
Given the following incomplete plan to make an onlette
1) Gather all necessary ingredients, including eggs, butter or oil, salt and pepper, cheese (optional), and any other desired fillings such as vegetables or meat.
2) Crack the eggs into a mixing bowl and whisk them together until the yolks are broken up. 
3) Add in the butter or oil to the egg mixture and continue to whisk until it is well combined.
4) Season with salt and pepper to taste.

Analyze the following 3 statements in terms of correctness and plausibility as a next step in the above plan:
[1] Use a spatula to gently lift one side of the omelette up towards the center so that the uncooked eggs can flow underneath. Repeat this process every few minutes as you continue to cook the egg mixture until it is mostly set but still slightly runny on top.
[2] Heat a non-stick skillet over medium heat and add enough butter or oil to coat the bottom of the pan. 
[3] Once the butter has melted, pour in the egg mixture and let it cook for about 30 seconds until it starts to set on the edges.
Output the number of the best statement.
[Output]
2

[Input]
Given the following incomplete plan to $goal
$current_plan
Analyze the following $n_options statements in terms of correctness and plausibility as a next step in the above plan:
$potential_next_steps
Output the number of the best statement.
[Output]
""")

planner_long = Template("""
[Input]
GOAL: Learn to swim
PLAN: None. Please start with a first step!
Output the next valid step for the above PLAN. If the PLAN is complete output DONE.

[Output]
Buy a swim suit
    
[Input]
GOAL: Boil an egg
PLAN:
    1) Get a pot
    2) Fill pot with enough water to cover the egg
Output the next valid step for the above PLAN. If the PLAN is complete output DONE.
[Output]
Get a needle and carefully pierce the egg

[Input]
GOAL: Eat ice cream
PLAN:
    1) Buy ice cream
    2) Eat ice cream
Output the next valid step for the above PLAN. If the PLAN is complete output DONE.
[Output]
DONE

[Input]
GOAL: $goal
PLAN: $current_plan
Output the next valid step for the above PLAN. If the PLAN is complete output DONE.
[Output]
""")


def make_plan_str(plan_steps):
    if len(plan_steps) == 0:
        return  "None. Please start with a first step!"
    current_plan = '\n'
    for n, step in enumerate(plan_steps):
        current_plan += "    " + str(n+1) + ') ' + step.get("task") + '\n'
        # current_plan += '-------------------------------------------\n'
        # current_plan += step.get("result") + '\n'
    return current_plan 

def make_planner_prompt(goal, plan_steps):
    current_plan = make_plan_str(plan_steps)
    prompt = planner_long.substitute(goal=goal, current_plan=current_plan)
    return prompt

def make_critic_prompt(goal, plan_steps, potential_next_steps):
    current_plan = make_plan_str(plan_steps)
    next_steps_list = ''.join(['[' + str(i+1) + '] ' + step + '\n' for i,step in enumerate(potential_next_steps)])  
    prompt = critic.substitute(goal=goal, n_options=len(potential_next_steps), current_plan=current_plan, potential_next_steps=next_steps_list)
    return prompt

def make_executive_prompt(goal, plan, task):

    return executer.substitute(goal=goal, task=task)