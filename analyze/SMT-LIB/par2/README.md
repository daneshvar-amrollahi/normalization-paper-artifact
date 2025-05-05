```
python3 generate_par2_mad.py ../../../SMT-LIB/wsp/z3/z3_wsp_smtlib.csv > z3_wpass_par2mad
python3 generate_par2_mad.py ../../../SMT-LIB/wsp/cvc5/cvc5_wsp_smtlib.csv > cvc5_wpass_par2mad

python3 generate_par2_mad.py ../../../SMT-LIB/nopass/z3/z3_nopass.csv > z3_nopass_par2mad
python3 generate_par2_mad.py ../../../SMT-LIB/nopass/cvc5/cvc5_nopass_smtlib.csv > cvc5_nopass_par2mad
```