import std.stdio;
import std.string;
import std.socket;


void main()
{
	auto sock = new Socket(AddressFamily.INET, SocketType.STREAM, ProtocolType.IP);
	sock.connect(new InternetAddress("0.0.0.0", 7777));
	char[4] buff = "asdf";
	sock.send(buff[]);
	sock.receive(buff[]);
	writeln(buff);
	sock.close();
}
