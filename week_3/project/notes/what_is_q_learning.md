**Q‑learning** is a model‑free, value‑based reinforcement‑learning (RL) algorithm that enables an autonomous agent to learn how to act optimally in an unknown environment by trial‑and‑error interaction.  

---

### Core Idea  

- The agent maintains a **Q‑function** \(Q(s,a)\) – an estimate of the expected cumulative reward (also called the *return*) it will receive when it takes action **a** in state **s** and thereafter follows the best possible policy.  
- By repeatedly updating this table (or approximator) from experience, the Q‑function converges to the *optimal action‑value function* \(Q^{*}(s,a)\). Once \(Q^{*}\) is known, the optimal policy is simply  

\[
\pi^{*}(s)=\arg\max_{a} Q^{*}(s,a).
\]

Because the update rule does **not** require a model of the environment’s dynamics (i.e., transition probabilities), Q‑learning is called **model‑free**. It is also **off‑policy**: the policy used to generate data (often an ε‑greedy exploratory policy) can differ from the policy being evaluated (the greedy policy derived from the current Q‑values).

---

### The Update Rule  

For each observed transition \((s_t, a_t, r_{t+1}, s_{t+1})\) the Q‑value is updated as  

\[
Q_{new}(s_t,a_t) \leftarrow Q(s_t,a_t) + \alpha \Big[ r_{t+1} + \gamma \max_{a'} Q(s_{t+1},a') - Q(s_t,a_t) \Big],
\]

where  

* **α** ∈ (0,1] – learning rate (how much new information overrides old).  
* **γ** ∈ [0,1] – discount factor (how future rewards are weighted).  
* The term \(r_{t+1} + \gamma \max_{a'} Q(s_{t+1},a')\) is the **temporal‑difference (TD) target**; the difference between the target and the current estimate is the **TD error**.

Repeated application of this rule under mild conditions (e.g., decaying α, sufficient exploration) guarantees convergence to \(Q^{*}\) for discrete, finite Markov Decision Processes (MDPs) [[Wikipedia](https://en.wikipedia.org/wiki/Q-learning)].

---

### Typical Algorithm (pseudo‑code)

```
Initialize Q(s,a) arbitrarily (e.g., zeros) for all states s and actions a
for each episode:
    initialise state s
    while s is not terminal:
        choose action a using an ε‑greedy policy derived from Q
        execute a, observe reward r and next state s'
        Q(s,a) ← Q(s,a) + α [ r + γ max_a' Q(s',a') – Q(s,a) ]
        s ← s'
```

* **Exploration vs. exploitation** – ε‑greedy (or softmax) adds randomness so the agent eventually tries every state‑action pair, which is required for convergence.  

* **Function approximation** – In large or continuous state spaces the Q‑table becomes impractical; neural networks (Deep Q‑Network, DQN) can be used to approximate \(Q(s,a)\) while retaining the same update principle.

---

### Why It Matters  

- **Simplicity** – The algorithm is easy to implement and understand, making it a standard introductory example for RL.  
- **Theoretical guarantees** – Convergence to the optimal action‑value function is proven for tabular cases.  
- **Foundation for extensions** – Many later RL breakthroughs (e.g., DQN, Double Q‑learning, Dueling networks) build directly on the Q‑learning update.

---

### References  

* **Wikipedia – “Q‑learning.”** Provides a concise definition and the tabular update rule. https://en.wikipedia.org/wiki/Q-learning  
* **GeeksforGeeks – “Q‑Learning in Reinforcement Learning.”** Offers a clear tutorial and Python example, emphasizing the model‑free, off‑policy nature. https://www.geeksforgeeks.org/machine-learning/q-learning-in-python/  
* **DataCamp tutorial – “An Introduction to Q‑Learning.”** Highlights the ε‑greedy exploration strategy and explains the role of the discount factor. https://www.datacamp.com/tutorial/introduction-q-learning-beginner-tutorial  

These sources collectively give the standard academic description of Q‑learning and its practical implementation details.