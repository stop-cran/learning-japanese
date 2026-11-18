"""Conservative full-article and individually complete optional-unit bounds."""
import math
from capacity011 import source_class as inherited_source_class


def source_class(name):
    name = name.split(" [", 1)[0]
    if name.startswith("evidence/kanjidic2-full-records/") and name.endswith(".xml"):
        return "full-kd-record", .60
    return inherited_source_class(name)


def source_tokens(name, raw):
    return math.ceil(len(raw) * source_class(name)[1])


def solo_envelope(raw):
    if not raw.endswith(b"\n"):
        raise ValueError("Source must end in LF")
    segments, size = 1, 0
    for line in raw.splitlines(keepends=True):
        if len(line) > 13900:
            raise ValueError("Source line exceeds bounded chain size")
        if size + len(line) > 13900:
            segments += 1
            size = 0
        size += len(line)
    return 2100 * (segments if len(raw) <= 13900 else segments + 1)


def extension_upper(sources):
    envelope = 2100 + sum(solo_envelope(raw) for _, raw, _ in sources)
    return {
        "payloadBytes": sum(len(raw) for _, raw, _ in sources),
        "envelopeBytesUpper": envelope,
        "tokens": sum(source_tokens(name, raw) for name, raw, _ in sources)
                  + math.ceil(envelope * .574),
    }


def chain_cost(chain, sources):
    payload = sum(len(raw) for _, raw, _ in sources)
    total = sum(row["bytes"] for row in chain["segments"])
    if total < payload:
        raise ValueError("Negative chain envelope")
    return {
        "payloadBytes": payload,
        "chainBytes": total,
        "envelopeBytes": total - payload,
        "tokens": sum(source_tokens(name, raw) for name, raw, _ in sources)
                  + math.ceil((total - payload) * .574),
    }
