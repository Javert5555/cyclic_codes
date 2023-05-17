from bitarray import bitarray

def encode_cyclic(msg, gen):
    # Convert the message and generator polynomials to bitarrays
    msg_bits = bitarray(msg)
    gen_bits = bitarray(gen)

    # Calculate the number of parity bits needed
    num_parity_bits = len(gen_bits) - 1

    # Append zeros to the message to make room for the parity bits
    msg_bits.extend([False] * num_parity_bits)

    # Calculate the initial remainder
    remainder = msg_bits[:len(gen_bits)]

    # Loop over the message, calculating the remainder at each step
    for i in range(len(gen_bits), len(msg_bits)):
        # XOR the remainder with the generator polynomial
        if remainder:
            remainder = remainder ^ gen_bits
        # Shift the remainder to the left and add the next bit of the message
        remainder = remainder[1:]
        remainder.append(msg_bits[i])

    # Return the original message with the parity bits appended
    return msg + remainder.to01()

# Example usage
msg = "1100"
gen = "1011"
encoded_msg = encode_cyclic(msg, gen)
print("Encoded message:", encoded_msg)

def decode_cyclic(encoded_msg, gen):
    # Convert the encoded message and generator polynomials to bitarrays
    encoded_bits = bitarray(encoded_msg)
    gen_bits = bitarray(gen)

    # Calculate the number of parity bits
    num_parity_bits = len(gen_bits) - 1

    # Calculate the initial remainder
    remainder = encoded_bits[:len(gen_bits)]

    # Loop over the encoded message, calculating the remainder at each step
    for i in range(len(gen_bits), len(encoded_bits)):
        # XOR the remainder with the generator polynomial
        if remainder:
            remainder = remainder ^ gen_bits
        # Shift the remainder to the left and add the next bit of the encoded message
        remainder = remainder[1:]
        remainder.append(encoded_bits[i])

    # Check if the remainder is zero
    if remainder.count() == num_parity_bits:
        return encoded_bits[:-num_parity_bits].to01()
    else:
        return None

# Example usage
encoded_msg = "101010110"
gen = "1101"
decoded_msg = decode_cyclic(encoded_msg, gen)
print("Decoded message:", decoded_msg)