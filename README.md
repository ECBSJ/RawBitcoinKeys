# RawBitcoinKeys

https://raw-keys.herokuapp.com/

## Update

(October 2023) This website above is no longer in service. Some time ago Heroku decided to withdraw their free service and I haven't had the chance to redeploy it onto a different provider. This was the first ever website I created using python's Flask web framework. It was extremely barebones.

## Summary

I created this non-mnemonic key generator through Flask that shows you the step-by-step process through the ECDSA and hashing algos leading you from the initial private key creation to your public address.

A RNG was purposely not used for the beginning step, don't be lazy.

The elliptic cryptography curve to convert the private key to a public key utilizes a python script taken from James D'Angelo (https://github.com/wobine/blackboard101/blob/master/EllipticCurvesPart4-PrivateKeyToPublicKey.py). The subsequent script used to convert the compressed public keys to a public address was pulled from https://gist.github.com/circulosmeos.

For an elaborate read on this process, feel free to check out this article: https://medium.com/tuoyuanresearch/getting-back-to-basics-an-oldie-but-goodie-e8169fecce01
