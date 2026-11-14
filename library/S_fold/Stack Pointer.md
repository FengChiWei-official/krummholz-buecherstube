## Definition

Holds the address of the top of the stack. On x86 the stack grows toward lower addresses, and `PUSH`, `POP`, `CALL` and `RET` change the pointer implicitly, so a frame is addressed as an offset from it rather than from an absolute address. The ABI does not treat RSP as a general register: a function must leave it exactly as it found it, which is what lets `RET` find the return address.

---
## **Related**

[[Register]] — the class it belongs to and the exception to its "general".
[[Program Counter]] — the other register a `CALL` writes without naming it.
[[Kernel Stack]] — the stack a syscall switches the pointer to.
[[Raw Index of Computer Systems]] — 登记主干
