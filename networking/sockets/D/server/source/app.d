import std.stdio;
import std.string;
import std.socket;


void main()
{
	auto sock = new Socket(AddressFamily.INET, SocketType.STREAM, ProtocolType.IP);
	sock.setOption(SocketOptionLevel.SOCKET, SocketOption.REUSEADDR, true);
	sock.bind(new InternetAddress("0.0.0.0", 7777));
	sock.listen(1);
	Socket incommingConn = sock.accept();

	char[4] buff;
	incommingConn.receive(buff[]);
	writeln(buff);

	buff = "OK.";
	incommingConn.send(buff[]);
	incommingConn.close();
	sock.close();
}
