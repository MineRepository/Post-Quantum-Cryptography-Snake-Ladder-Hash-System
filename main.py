
BOARD_SIZE = 256

cell_effects = [
#  1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16
   0,   0,   0,  25,   0,   0,   0,   0,   0,   0,   0,   0,  38,   0,   0,   0,
#  17   18   19   20   21   22   23   24   25   26   27   28   29   30   31   32
   0,   0,   0,   0,   0, -19,   0,   0,  17,   0,   0,   0,   0,   0, -17,   0,
#  33   34   35   36   37   38   39   40   41   42   43   44   45   46   47   48
   0,   0,   0,   0,   0,  76,  14,   0,   0,   0,   0,   0,   0,   0,   0,   0,
#  49   50   51   52   53   54   55   56   57   58   59   60   61   62   63   64
   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
#  65   66   67   68   69   70   71   72   73   74   75   76   77   78   79   80
   0,   0,   0,   0,   0,   0,   0,  21,   0,   0,   0,   0,   0,   0,   3,  44,
#  81   82   83   84   85   86   87   88   89   90   91   92   93   94   95   96
   0,   0,   0,   0,   0,   0,   0,   0,   0, -30, -34,   0,   0,   0,   0,   0,
#  97   98   99  100  101  102  103  104  105  106  107  108  109  110  111  112   
   0,   0,   0, -90,   0,   0,   0,   0,   0,   0,   0, -66,   0,   0,   0,   0,
# 113  114  115  116  117  118  119  120  121  122  123  124  125  126  127  128
   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, -60,
# 129  130  131  132  133  134  135  136  137  138  139  140  141  142  143  144
   0,  50,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
# 145  146  147  148  149  150  151  152  153  154  155  156  157  158  159  160 
   0,   0,   0,   0,   0,  50,   0,   0,   0,   0,   0,   0,   0,   0,   0,  60,
# 161  162  163  164  165  166  167  168  169  170  171  172  173  174  175  176
   0,   0,   0,   0,   0,   0,   0,   0,   0,  70,   0,   0,   0,   0,   0,   0,
# 177  178  179  180  181  182  183  184  185  186  187  188  189  190  191  192
   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  55,   0,   0,
# 193  194  195  196  197  198  199  200  201  202  203  204  205  206  207  208
   0,   0,   0,   0,   0,   0,   0, -50,   0,   0,   0,   0,   0,   0,   0,   0,
# 209  210  211  212  213  214  215  216  217  218  219  220  221  222  223  224
   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, -50,   0,   0,   0,   0,
# 225  226  227  228  229  230  231  232  233  234  235  236  237  238  239  240
   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, -50,
# 241  242  243  244  245  246  247  248  249  250  251  252  253  254  255  256
   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, -56
]

PADDING_SOURCE = "G@ul$h4N#Rz!aQ&7^Xv*Kp%2mW~eT+8nYb=Fj<3oU>Ls|9Dh{Ci}Aw[Bq]Ep(Or)Mu0Sv"

message    = input("\nEnter Message     : ")
hash_bytes = int(input("Hash size (bytes) : "))

msg_bytes = list(message.encode('utf-8'))
print(f"\nMessage bytes : {len(msg_bytes)}")
print(f"Hash size     : {hash_bytes} bytes") 

padding_bytes = list(PADDING_SOURCE.encode('utf-8'))

num_blocks = hash_bytes

block_size = (len(msg_bytes) + num_blocks-1) // num_blocks

total_bytes_needed = num_blocks * block_size

padded_msg = msg_bytes[:]
pi = 0
while len(padded_msg) < total_bytes_needed:
    padded_msg.append(padding_bytes[pi % len(padding_bytes)])
    pi += 1

print(f"Number of blocks  : {num_blocks}")
print(f"Block size        : {block_size} bytes")

blocks = []
for i in range(num_blocks):
    block = padded_msg[i * block_size : (i + 1) * block_size]
    blocks.append(block)


def move_on_board(position, dice):
    new_pos = position + dice
    new_pos = ((new_pos - 1) % BOARD_SIZE) + 1
    new_pos = new_pos + cell_effects[new_pos - 1]
    if new_pos < 1 or new_pos > BOARD_SIZE:
        new_pos = ((new_pos - 1) % BOARD_SIZE) + 1
    return new_pos

def process_block(block):
    position = block[0]
    for byte_val in block[1:]:
        bits     = format(byte_val, '08b')
        dice1    = int(bits[0:4], 2) + 1
        position = move_on_board(position, dice1)
        dice2    = int(bits[4:8], 2) + 1
        position = move_on_board(position, dice2)
    return position


print("\n--- Block Results ---")
block_positions = []
for i, block in enumerate(blocks):
    final_pos = process_block(block)
    block_positions.append(final_pos)
    print(f"  Block {i+1:3d}  ->  Final position: {final_pos:3d}  ->  Binary: {format(final_pos, '08b')}")

print("\n--- Left Rotate & Concatenate ---")
final_bits = ""
xor_accumulator = 0

for i, pos in enumerate(block_positions):
    shift   = i % 8
    bits    = format(pos, '08b')
    rotated = bits[shift:] + bits[:shift]
    final_bits += rotated

    xor_accumulator ^= int(rotated, 2)

    print(f"  Block {i+1}  ->  Pos: {pos}  ->  Original: {bits}  ->  Rotated: {rotated}  ->  XOR so far: {format(xor_accumulator, '08b')}")

final_bits = final_bits[:hash_bytes * 8]

final_number_before_xor = int(final_bits, 2)
xor_key = 0
for i in range(hash_bytes):
   
    xor_key = (xor_key << 8) | ((xor_accumulator ^ (i * 37)) & 0xFF)

final_number_after_xor = final_number_before_xor ^ xor_key
final_bits = format(final_number_after_xor, f'0{hash_bytes * 8}b')

print(f"\n  XOR accumulator   : {format(xor_accumulator, '08b')}")
print(f"  XOR key           : {format(xor_key, f'0{hash_bytes * 8}b')}")
print(f"  After XOR mixing  : {final_bits}")

final_number = int(final_bits, 2)
final_hex    = hex(final_number)[2:]

print(f"\n  Concatenated bits : {final_bits}")
print(f"  Total bit length  : {len(final_bits)} bits")
print("\n" + "=" * 45)
print(f"\n  FINAL OUTPUT (binary) :")
print(f"  {final_bits}")
print(f"\n  FINAL OUTPUT (hex) :")
print(f"  {final_hex}")