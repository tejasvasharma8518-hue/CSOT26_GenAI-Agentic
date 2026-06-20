**Answer**

Transformer attention is the core mechanism that lets a transformer‑style neural network (the architecture behind BERT, GPT, LLaMA, etc.) decide **which parts of the input sequence are most relevant to each other** when it builds its internal representations.  
It does this by computing, for every token (or image patch, audio frame, …) a weighted mixture of **all the other tokens** in the same sequence. The weights—called **attention scores**—are learned from data and are recomputed at every layer, so the model can dynamically focus on different contexts as the processing deepens.

Below is a concise, research‑oriented description that pulls together the most reliable web‑based explanations and the recent academic insight from the 2025 paper *“What are you sinking? A geometric approach on attention sink.”*  

---

### 1. The basic mathematics (self‑attention)

1. **Input embeddings**  
   Each token \(x_i\) is first projected into three vectors by learned linear maps:  
   \[
   \mathbf{q}_i = \mathbf{W}_Q x_i \quad
   \mathbf{k}_i = \mathbf{W}_K x_i \quad
   \mathbf{v}_i = \mathbf{W}_V x_i
   \]
   – **Query (Q)**, **Key (K)** and **Value (V)** matrices.

2. **Score computation**  
   For a pair of tokens \(i\) (query) and \(j\) (key) the raw compatibility is the scaled dot‑product:  
   \[
   s_{ij}= \frac{\mathbf{q}_i^\top \mathbf{k}_j}{\sqrt{d_k}}
   \]
   where \(d_k\) is the dimension of the key vectors (the scaling stabilises gradients).

3. **Softmax normalisation**  
   The scores are turned into a probability distribution over all tokens:  
   \[
   \alpha_{ij}= \frac{\exp(s_{ij})}{\sum_{j'=1}^{n}\exp(s_{ij'})}
   \]
   \(\alpha_{ij}\) is the **attention weight** – how much token *i* “looks at’’ token *j*.

4. **Weighted sum (output of one head)**  
   \[
   \mathbf{z}_i = \sum_{j=1}^{n} \alpha_{ij}\,\mathbf{v}_j
   \]
   \(\mathbf{z}_i\) is the new representation of token *i*, now containing information from the whole sequence, emphasised according to the learned weights.

5. **Multi‑head extension**  
   The process above is performed in parallel *h* times with independent \((\mathbf{W}_Q,\mathbf{W}_K,\mathbf{W}_V)\) matrices, yielding *h* “heads”. Their outputs are concatenated and linearly projected once more. Multi‑head attention lets the model capture different relational patterns simultaneously (e.g., syntax vs. semantics).

The whole block (multi‑head attention + residual connection + layer normalisation) is repeated many times (12‑96 layers in typical LLMs), each layer refining the context‑aware representations.

*Sources*: IBM’s overview of attention mechanisms notes that transformers “direct deep learning models … to focus on the most relevant parts of input”【0†title】; the Wikipedia entry on Transformers describes the multi‑head attention core【4†title】; Medium’s tutorial explains the token‑wise weighting process【5†title】.

---

### 2. Why attention matters – the intuitive picture

- **Dynamic focus**: Unlike fixed‑size convolution kernels, attention can attend to *any* other position, irrespective of distance. This lets the model capture long‑range dependencies (e.g., subject‑verb agreement across many words) efficiently.
- **Content‑based addressing**: The query‑key similarity measures *what* is being looked for, not *where* it is, so the same pattern can be recognised anywhere in the sequence.
- **Parallelism**: All pairwise scores are computed simultaneously using matrix multiplications, which GPUs/TPUs can execute very fast.

---

### 3. Recent research nuance – “attention sink” phenomenon

The 2025 paper *“What are you sinking? A geometric approach on attention sink”* (Ruscio et al.) adds a deeper geometric interpretation of how attention behaves in practice:

| Observation | Interpretation |
|-------------|----------------|
| **Attention sink (AS)** – certain tokens (often the special `[CLS]` token, position anchors, or punctuation) attract a disproportionately large fraction of attention from all other tokens. | The authors argue that AS reflects the emergence of **reference frames** in the high‑dimensional representation space. These frames act as geometric “anchors” that stabilise the coordinate system the model builds during training. |
| **Three reference‑frame types** – *centralized* (single anchor), *distributed* (multiple anchors), *bidirectional* (mutual anchoring). | Different architectural choices (e.g., absolute vs. rotary positional encodings) bias the model toward one of these frame structures, influencing which tokens become sinks. |
| **Early‑training emergence** – reference frames appear in the first few thousand optimisation steps, before downstream performance spikes. | Suggests that attention sinks are not bugs but **optimal solutions** to the problem of establishing a stable internal coordinate system for the sequence. |
| **Design implications** – altering positional encodings or adding explicit “anchor‑regularisation” can control the strength or location of attention sinks, potentially improving interpretability or reducing unwanted bias. | Provides a concrete lever for model architects to shape attention behaviour beyond the generic multi‑head formulation. |

*Take‑away*: While the classic description of transformer attention focuses on the query‑key‑value algebra, the attention‑sink literature shows that **global patterns in the attention matrix have a geometric meaning**—they are the model’s way of grounding abstract token vectors to a shared reference frame. This insight complements the standard textbook view and opens avenues for systematic architecture engineering.

*Source*: Paper summary and AI‑generated abstract (2025) describe the attention sink as a “manifestation of a fundamental geometric principle… establishing reference frames”【2508.02546】.

---

### 4. Putting it together – a concise definition

> **Transformer attention** is a differentiable, content‑based weighting mechanism that, for each element of an input sequence, computes a weighted sum of value vectors from *all* elements based on the similarity of learned query and key vectors. Implemented as **multi‑head scaled dot‑product attention**, it enables the network to flexibly model long‑range dependencies, and, as recent work shows, it also gives rise to systematic “attention‑sink” patterns that correspond to emergent geometric reference frames within the model’s latent space.

---

### 5. References (formatted for a quick bibliography)

1. IBM. *What is an attention mechanism?* (2024). https://www.ibm.com/think/topics/attention-mechanism  
2. Wikipedia. *Transformer (deep learning)*. https://en.wikipedia.org/wiki/Transformer_(deep_learning)  
3. Stefan B. Schneider. *Understanding Transformers and Attention* (Medium, 2023). https://medium.com/@stefanbschneider/understanding-attention-and-transformers-d84b016cd352  
4. Ruscio, V.; Nanni, U.; Silvestri, F. **What are you sinking? A geometric approach on attention sink**. arXiv:2508.02546, 2025. https://arxiv.org/abs/2508.02546  

These sources collectively give a complete picture of what attention is, how it works mathematically, why it is useful, and what recent research reveals about its deeper geometric behavior.