#define PACKET_SIZE 20
#define BITS_PER_BYTE 8

struct BlePacket {
	/* Start packet header */
	// Highest 4 bits: packet type ID, lowest 4 bits: number of padding bytes
	byte metadata;
	uint16_t seqNum;
	/* End packet header */
	/* Start packet body */
	// 16-bytes of data, e.g. accelerometer data
	byte data[16];
	/* End packet body */
	/* Start footer */
	byte checksum;
	/* End footer */
};

enum packetIds {
	HELLO = 0,
	ACK = 1,
	P1_IMU = 2,
	P1_IR_RECV = 3,
	P1_IR_TRANS = 4,
	P2_IMU = 5,
	P2_IR_RECV = 6,
	P2_IR_TRANS = 7,
	GAME_STAT = 8
};

bool isPacketValid(BlePacket &packet) {
  // TODO: Implement actual checks
  return true;
}

/* void convertBytesToPacket(String dataBuffer, BlePacket &packet) {
  byte packetType = dataBuffer.charAt(0);
  short packetId = 
} */