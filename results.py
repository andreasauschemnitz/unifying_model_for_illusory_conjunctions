import matplotlib.pyplot as plt

plt.xticks([0,1,2],("correct perception","illusory conjunction","hallucination"))
plt.axis([-0.5,2.5,0,1])

v_treisman = [0.49,0.37,0.14]
v_full = [1,0,0]
v_divided = [0.23,0.77,0]
v_partial = [0.55,0.45,0]
v_guess = [0.12,0.22,0.66]

plt.plot(v_treisman,"ro-",label="experiment Treisman")
plt.plot(v_full,"c+-",label="full attention")
plt.plot(v_divided,"b^-",label="divided attention")
plt.plot(v_partial,"g*-",label="final model")
plt.plot(v_guess,"ys-",label="random guess")

plt.ylim([-0.03,1.03])
plt.legend()

plt.show()


