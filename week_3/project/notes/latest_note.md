**Reinforcement Learning (RL) – A concise research‑level definition**

Reinforcement learning is a **branch of machine‑learning** in which an *autonomous agent* learns to make sequential decisions by **interacting with an environment** and receiving feedback in the form of scalar rewards.  
The agent’s goal is to discover a *policy*—a mapping from states to actions—that **maximizes the expected cumulative (discounted) reward** over time.  

| Component | What it means in RL | Key references |
|-----------|--------------------|----------------|
| **Agent** | The decision‑making entity that selects actions. | GeeksforGeeks, IBM |
| **Environment** | Everything external to the agent; it receives the agent’s actions, returns a new state and a reward. | GeeksforGeeks, AWS |
| **State (s)** | A representation of the current situation of the environment as perceived by the agent. | GeeksforGeeks |
| **Action (a)** | A possible move the agent can take in a given state. | AWS |
| **Reward (r)** | Immediate scalar feedback that signals how good the last action was. | IBM |
| **Policy (π)** | A (deterministic or stochastic) rule that tells the agent which action to choose in each state. | Google Cloud |
| **Objective** | Maximize the **expected return** \( G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1} \) where \( \gamma \in [0,1] \) is a discount factor. | Standard RL theory |

### How learning happens
1. **Trial‑and‑error (exploration)** – The agent initially tries actions that may be sub‑optimal to gather information about the environment.  
2. **Feedback (exploitation)** – Using the observed rewards, the agent updates its internal value estimates (e.g., state‑value \(V(s)\) or action‑value \(Q(s,a)\)) and gradually prefers actions that have yielded higher returns.  
3. **Iterative improvement** – Over many episodes the policy converges toward the optimal one (π*), achieving the highest possible expected return.  

### Why RL is distinct from other ML paradigms
- **No labeled input‑output pairs** (as in supervised learning); the only supervision comes from the scalar reward signal.  
- **Sequential decision making**: actions affect not only immediate reward but also future states and rewards, requiring planning and credit assignment over time.  
- **Model‑free vs. model‑based**: many RL algorithms (e.g., Q‑learning, policy gradients) learn directly from experience without an explicit model of the environment’s dynamics, whereas model‑based methods first learn a transition model and then plan.

### Supporting literature

| Source | Summary of definition |
|--------|----------------------|
| **GeeksforGeeks – “What is Reinforcement Learning?”** | Describes RL as “a branch of machine learning that focuses on how agents can learn to make decisions through trial and error to maximize …”【0†snippet】 |
| **AWS – “What is Reinforcement Learning?”** | Calls RL “a machine‑learning technique that trains software to make decisions to achieve the most optimal results.”【0†snippet】 |
| **IBM – “What is reinforcement learning?”** | States that RL “is a type of machine learning process in which autonomous agents learn to make decisions by interacting with their environment.”【0†snippet】 |
| **Google Cloud – “What is reinforcement learning (RL)?”** | Defines RL as “a type of machine learning where an ‘agent’ learns optimal behavior through interaction with its environment.”【0†snippet】 |

### Academic perspective (illustrative)

The paper **“A Definition of Happiness for Reinforcement Learning Agents”** (Daswani & Leike, 2015) treats RL agents as entities that experience *temporal‑difference (TD) error*—the discrepancy between expected and obtained reward—as a quantitative signal of “happiness”.  This highlights a **core RL concept**: the agent continually updates expectations based on the difference between predicted and actual rewards, which is precisely the learning signal driving policy improvement. 【1†summary】  

---

**Bottom‑line:** Reinforcement learning equips an agent with a **closed‑loop learning system**—sense → act → receive reward → update policy—so that, purely through interaction, it discovers how to behave optimally in environments where the correct actions are not prescribed in advance.