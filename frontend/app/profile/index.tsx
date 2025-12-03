import { View, Text, StyleSheet } from "react-native";
import GradientBackground from "@/components/GradientBackground";

export default function Profile() {
  return (
    <GradientBackground>
      <View style={styles.container}>
        <Text style={styles.text}>Profile</Text>
      </View>
    </GradientBackground>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  text: {
    fontSize: 24,
    fontWeight: "bold",
  },
});
