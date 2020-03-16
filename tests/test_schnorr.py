import unittest

from hypothesis import given, assume

from electionguard.elgamal import ElGamalKeyPair
from electionguard.group import ElementModQ, g_pow, ElementModP
from electionguard.schnorr import make_schnorr_proof, valid_schnorr_transcript, SchnorrProof
from tests.test_elgamal import arb_elgamal_keypair
from tests.test_group import arb_element_mod_q_no_zero, arb_element_mod_p_no_zero


class TestSchnorr(unittest.TestCase):
    def test_schnorr_proofs_simple(self):
        # doesn't get any simpler than this
        keypair = ElGamalKeyPair(ElementModQ(2), g_pow(ElementModQ(2)))
        nonce = ElementModQ(1)
        proof = make_schnorr_proof(keypair, nonce)
        self.assertTrue(valid_schnorr_transcript(proof, keypair.public_key))

    @given(arb_elgamal_keypair(), arb_element_mod_q_no_zero())
    def test_schnorr_proofs_valid(self, keypair: ElGamalKeyPair, nonce: ElementModQ):
        proof = make_schnorr_proof(keypair, nonce)
        self.assertTrue(valid_schnorr_transcript(proof, keypair.public_key))

    # Now, we introduce errors in the proofs and make sure that they fail to verify
    @given(arb_elgamal_keypair(), arb_element_mod_q_no_zero(), arb_element_mod_q_no_zero())
    def test_schnorr_proofs_invalid_r(self, keypair: ElGamalKeyPair, nonce: ElementModQ, other: ElementModQ):
        proof = make_schnorr_proof(keypair, nonce)
        assume(other != proof.r)
        proof2 = SchnorrProof(proof.V, other, proof.c)
        self.assertFalse(valid_schnorr_transcript(proof2, keypair.public_key))

    @given(arb_elgamal_keypair(), arb_element_mod_q_no_zero(), arb_element_mod_p_no_zero())
    def test_schnorr_proofs_invalid_public_key(self, keypair: ElGamalKeyPair, nonce: ElementModQ, other: ElementModP):
        proof = make_schnorr_proof(keypair, nonce)
        assume(other != keypair.public_key)
        self.assertFalse(valid_schnorr_transcript(proof, other))
