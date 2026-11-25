"""CO5 Task A2: Application Protocols (SMTP, POP3 vs IMAP, FTP/SFTP, SNMP, DNS/HTTP)."""


def main():
    print("=== CO5 TASK A2: FOLLOW THE APPLICATION PROTOCOLS ===")
    print("A2.1 — SMTP Command Sequence & Reply Codes:")
    smtp_seq = [
        ("S: 220 mail.learn.edu ESMTP Ready", "Server greeting"),
        ("C: EHLO student-laptop.local", "Client identifies itself"),
        ("S: 250-mail.learn.edu Hello", "Server accepts EHLO"),
        ("C: MAIL FROM:<santhosh@learn.edu>", "Envelope sender"),
        ("S: 250 2.1.0 Ok", "Sender accepted"),
        ("C: RCPT TO:<faculty@learn.edu>", "Envelope recipient"),
        ("S: 250 2.1.5 Ok", "Recipient accepted"),
        ("C: DATA", "Start message body"),
        ("S: 354 End data with <CR><LF>.<CR><LF>", "Ready for payload"),
        ("C: Subject: Lab Report\\r\\n...\\r\\n.", "Body terminated with '.'"),
        ("S: 250 2.0.0 Ok: queued as A1B2C", "Message queued"),
        ("C: QUIT", "Close session"),
        ("S: 221 2.0.0 Bye", "Connection closed"),
    ]
    for line, note in smtp_seq:
        print(f"  {line:<42} ({note})")
    print("  POP3 (delete after download) vs IMAP: POP3 deletes mail from server after phone downloads it ->")
    print("    laptop and lab PC never see it. IMAP keeps folders/flags synchronised on the server across all devices.")

    print("\nA2.2 — Active vs Passive FTP, SFTP/HTTPS & SNMP:")
    print("  - Active FTP fails : Client opens control TCP/21; server initiates data TCP/20 BACK to client's ephemeral port -> blocked by NAT/firewall.")
    print("  - Passive FTP works: Client sends PASV and initiates BOTH control and data connections outbound.")
    print("  - SFTP / HTTPS     : Encrypts credentials & payload (FTP transmits passwords & data in plaintext).")
    print("  - SNMP GET         : Manager polls OID 1.3.6.1.2.1.2.2.1.10.1 (ifInOctets.1) via UDP/161; agent replies GetResponse.")
    print("  - SNMP TRAP        : Router proactively sends unsolicited UDP/162 linkDown (OID 1.3.6.1.6.3.1.1.5.3) on link failure.")

    print("\nA2.3 — Browser DevTools Slow-Page Timings:")
    print("  - 'DNS Lookup' (>100 ms) indicates uncached/slow resolver; 'Waiting (TTFB)' indicates backend/DB/TLS stall;")
    print("    'Content Download' indicates large unbundled payloads or low throughput.")

    print("\n--- Alternative Concept Analysis: Webmail HTTPS vs IMAP (50 Messages) ---")
    print("  - IMAP (headers first): 50 headers x ~1 KB = ~50 KB; fetches bodies only when clicked.")
    print("  - Webmail HTTPS       : HTML/JS/CSS framework (~1-2 MB) + 50 JSON summaries (~100 KB), but easily cached.")
    print("  - Easier to secure    : Webmail HTTPS (single port 443, modern OAuth2/MFA/CSP/WAF without exposing IMAP 993).")


if __name__ == "__main__":
    main()
