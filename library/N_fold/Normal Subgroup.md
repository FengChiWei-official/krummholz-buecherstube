## define

A [[Subgroup]] $\mathbf{N}$ of Group $\mathbf{G}$ is a [[Normal Subgroup]],  
if $\forall a \in N$,  $\forall g \in \mathbf{G}$, 
then the [[Conjugate]] $gag^{-1} \in N$


## Trick
[[Automorphism]] $C_a: G \to G$,  $C_a(x) = axa^{-1}$   （也写作 $x^a$）
1. $C_a \in \mathrm{Aut}(G)$;  $C_a^{-1} = C_{a^{-1}}$;  $C_{ab} = C_a \circ C_b$
2. $N \vartriangleleft G \iff C_a(N) = N\ \ \forall a \in G$   （只需证 $\subseteq$）
3. $N \vartriangleleft G \Rightarrow C_a|_N \in \mathrm{Aut}(N)$
4. $\ker(a \mapsto C_a) = Z(G)$

Example: $S_3$ 里 $A_3$（非平凡互换）vs $\{e,(12)\}$（像跑出 $N$）；阿贝尔群 ⇒ $C_a = \mathrm{id}$

---
## **related**：
### reorganization

[[Attribution Theorem of Kernel - Kernel is Normal Subgroup]]
[[Proposition of all Subgroup of Abelian Group is Normal Group]]
[[Center of a Group Z| Center is always the Normal group]]

## Introduced Concept

[[Center of a Group Z]]
