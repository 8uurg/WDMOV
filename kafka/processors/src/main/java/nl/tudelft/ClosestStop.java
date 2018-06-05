package nl.tudelft;

import nl.tudelft.JsonPOJOSerializer;
import nl.tudelft.JsonPOJODeserializer;

import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.ValueMapper;
import org.apache.kafka.streams.Consumed;
import org.apache.kafka.streams.kstream.Produced;

import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.common.serialization.Deserializer;

import java.util.Arrays;
import java.util.Properties;
import java.util.concurrent.CountDownLatch;
import java.util.HashMap;
import java.util.Map;

/**
 * This program processes the incoming stream of JSON serialized public
 * transport stops, and reduces the stream to the stop that is closest
 * to some hardcoded coordinates (the query).
 */
public class ClosestStop {

    // POJO classes
    static public class Stop {
        public String id;
        public String name;
        public double latitude;
        public double longitude;

        /**
         * Approximate distance between polar coordinates as Euclidian distance.
         * @param lat Latitude coordinate
         * @param lon Longitude coordinate
         * @return The distance between the stop location and the specified location
         */
        public double distanceTo(double lat, double lon) {
            return Math.sqrt(Math.pow(latitude - lat, 2) + Math.pow(longitude - lon, 2));
        }

        public double distance() {
            return distanceTo(51.99905, 4.3738);
        }
    }

    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-closest-stop");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());


        // Construct JSON Serde
        Map<String, Object> serdeProps = new HashMap<>();

        final Serializer<Stop> JsonPOJOSerializer = new JsonPOJOSerializer<>();
        serdeProps.put("JsonPOJOClass", Stop.class);
        JsonPOJOSerializer.configure(serdeProps, false);

        final Deserializer<Stop> JsonPOJODeserializer = new JsonPOJODeserializer<>();
        serdeProps.put("JsonPOJOClass", Stop.class);
        JsonPOJODeserializer.configure(serdeProps, false);

        final Serde<Stop> jsonSerde = Serdes.serdeFrom(JsonPOJOSerializer, JsonPOJODeserializer);

        // Build processor topology
        final StreamsBuilder builder = new StreamsBuilder();

        KStream stops = builder.stream("streams-stops-input", Consumed.with(Serdes.String(), jsonSerde));

        KStream closestStops = stops.groupByKey(Serdes.String(), jsonSerde)
                .reduce(
                        (agg, val) -> ((Stop) val).distance() < ((Stop) agg).distance() ? val : agg
                )
                .toStream();

        closestStops.to("streams-closest-stop-output", Produced.with(Serdes.String(), jsonSerde));

        final Topology topology = builder.build();
        System.out.println(topology.describe());
        final KafkaStreams streams = new KafkaStreams(topology, props);
        final CountDownLatch latch = new CountDownLatch(1);

        // attach shutdown handler to catch control-c
        Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
            @Override
            public void run() {
                streams.close();
                latch.countDown();
            }
        });

        try {
            streams.start();
            latch.await();
        } catch (Throwable e) {
            System.exit(1);
        }
        System.exit(0);
    }
}
